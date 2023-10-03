# -*- coding: utf-8 -*-
"""
Read and write binary data to and from Pandas DataFrames.

Created on Wed Sep 20 15:27:01 2023

@author: Jamie Cash
"""

from enum import Enum
import numpy as np
import pandas as pd
from typing import List, Dict
import struct


class ByteOrder(Enum):
    """
    The order of bytes in a variable. Can be ByteOrder.LITTLE for little endian
    or ByteOrder.BIG for big endian.
    """
    LITTLE = 'little'
    BIG = 'big'

    
class Variable:
  """
  The metadata for a single variable.

  Arguments:
    name (str): The name of the variable.
    size (int): The size of the variable in bytes.
    datatype (type): The datatye of the variable.
    offset (int, optional): The byte offset where the variable starts.
      If not specified, this will be calculated by Structure.
    byteorder (ByteOrder, optional): Whether the variable has a  little or big
      endian byte order. Default is ByteOrder.LITTLE.
    signed (bool, optional): Whether the variable is signed. Default is false.
  """
  name: str
  size: int
  datatype: type
  offset: int
  byteorder: ByteOrder
  signed: bool

  def __init__(self, name:str, size:int, datatype:type, offset:int=None,
               byteorder:ByteOrder=ByteOrder.LITTLE, signed:bool=False):
    self.name = name
    self.size = size
    self.datatype = datatype
    self.offset = offset
    self.byteorder = byteorder
    self.signed = signed

  @property
  def next_offset(self):
    """
    Gets the offset of the next variable.
    """
    return self.offset + self.size

  def __len__(self):
    """
    The length of the variable.
    """
    return self.size

  def __repr__(self):
    return f"name: {self.name}, offset: {self.offset}, size: {self.size}, " \
      f"datatype: {self.datatype}, byteorder: {self.byteorder}, " \
      f"signed: {self.signed}"
      
      
class Structure:
  """
  The definition of a data structure.
  
  Arguments:
    start (int): The start position of the data structure.
    variables (List of Variable): The definitions of all variables in the
      structure.
    rows (int, optional): If the data structure is repeating, specifies the
      number of times that it repeats. Default is 1 for a non repeating
      structure.
  """
  start: int
  variables:  List[Variable]
  rows: int

  def __init__(self, start:int, variables:List[Variable], rows:int=1):
    self.start = start
    self.variables = variables
    self.rows = rows

    # Calculate any missing variable offsets.
    last = None
    for variable in self.variables:
      if variable.offset is None:
        if last is None:
          variable.offset = self.start
        else:
          variable.offset = last.next_offset

      last = variable

  def __len__(self):
    """
    Length of the structure. This is the sum of the size of all variables
    multipled by the number of rows.
    """
    return sum([len(i) for i in self.variables]) * self.rows

  def __repr__(self):
    return f"start: {self.start}, rows: {self.rows}, variables: " + \
        f"{self.variables}"



class DataHandler:
  """
  Reads and writes binary data to and from pandas DataFrames using the 
  specification provided in [structures].

  Arguments:
      data (bytes): The data.
      structures (dict of str, Structure, optional): The specification of any 
        data structures. The dict key is the name of the structure that will 
        be used when reading and updating. Additional structures can be addes
        later using [add_structure]. If no structures are specified, then 
        read_structure and write_structure cannot be used, however DataHandler
        can still be used to read and write variables.
      str_encode (str, optional): The string encoding. See 
        https://docs.python.org/3/library/codecs.html#standard-encodings for 
        a list of all encodings. Default is utf-8.
  """

  __data: bytes
  __structures: Dict[str, Structure] = None
  __str_encode: str

  def __init__(self, data: bytes, structures: Dict[str, Structure]=None, 
               str_encode='utf-8'):
    self.__data = data
    self.__str_encode = str_encode

    # Add the structures individually to benifit for boundary checks.
    if structures is not None:
      for structure_name in structures.keys():
        self.add_structure(structure_name, structures[structure_name])


  @property
  def data(self):
    return self.__data
  
  def add_structure(self, name: str, structure: Structure):
    """
    Adds a structure.

    Arguments:
      name (str): The name of the structure to add. If structure already exists 
        with that name, it will be overwritten.
      structure (Structure): The structure to add.
    """
    # Check that the structure is within the bounds of the data
    self.__check_bounds(structure.start, len(structure))

    # Create the structure if not already created and add the structure.
    if self.__structures is None:
      self.__structures = {name: structure}
    else:
      self.__structures[name] = structure

  def read_hex(self, start: int=0, length: int=None, seperator: str=':') -> str:
    """
    Returns data as a easily readable string of hexadecimal 
    characters.

    Arguments:
      start (int, optional): The starting postion to read from. Default is the
        first byte of the data.
      length (int, optional): The number of bytes to return. Default is the 
        number of bytes available to read in the data given the specified 
        [start].
      seperator (str, optional): The seperator character for hex bytes. Default 
        is ':'.

    Returns:
      (str): The bytes as a string of hexadecimal byte representations seperated 
        by [seperator].
    """
    # Calculate and set length if not specified.
    if length is None:
      length = len(self.data) - start

    # Check that bounds
    self.__check_bounds(start, length)
    
    # Return the data as a hex string
    return self.data[start:start+length].hex(seperator)

  def read_structure(self, name: str) -> pd.DataFrame:
    """
    Reads this instances [data] into a dataframe using the specification 
    provided by [structures].

    Arguments:
      name (str): The name of the structure to read.

    Returns:
      (DataFrame): The dataframe containing the converted data from the
      structure.
    """
    # Assert that structure exists.
    assert self.__structures is not None, "There are no structures defined."
    assert name in self.__structures, f"Structure with name '{name}' does not "\
      + "exist. Add it using [add_structure] before reading."

    # Get the structure
    structure = self.__structures[name]

    # Iterate rows and variables, building up the data
    data = []
    for row in range(structure.rows):
      row_data = []
      for var in structure.variables:
        # Get data for the variable and add to row

        # Get the offset for the row. This is the size of the row * the row 
        # num.
        offset = int(row * len(structure) / structure.rows)

        # Get the data for the row
        row_data.append(self.read_variable(var, offset))
      data.append(row_data)

      # Get the column names
      columns = []
      for var in structure.variables:
        columns.append(var.name)

    # Create the dataframe and return it
    df = pd.DataFrame(data=data, columns=columns)
    return df
    
  def read_variable(self, variable:Variable, offset:int=None) -> object:
    """
    Reads a variable from [data] and converts it to the data type specified in
    the [variable].

    Arguments:
      variable (Variable): The name of the variable to read.
      offset (int, optional): Offset to apply. Added to variable offset. Used
        to read repeating structures. If not specified, then no offset is 
        applied.

    Returns:
      object: The data converted to the data type specified in [variable].
    """

    # Get the data as bytes
    full_offset = variable.offset if offset is None else variable.offset + \
        offset
    self.__check_bounds(full_offset, variable.size)
    bytes_data = self.__read(full_offset, variable.size)

    # Convert it to the correct data type
    converted_data = None
    #print(f"variable.byteorder as str: {str(variable.byteorder)}")
    if variable.datatype == int:
      converted_data = int.from_bytes(bytes_data,
                                      byteorder=variable.byteorder.value,
                                      signed=variable.signed)
    elif variable.datatype == str:
      converted_data = (str( bytes_data.decode(self.__str_encode)))
    elif variable.datatype == bool:
      converted_data = bool.from_bytes(bytes_data,
                                       byteorder=variable.byteorder.value,
                                       signed=variable.signed)
    elif variable.datatype == float:
      endian_sign = '<' if variable.byteorder == ByteOrder.LITTLE else '>'
      converted_data = struct.unpack(f'{endian_sign}f', bytes_data)[0]
    else:
       # For any other datatype, keep as bytes.
       converted_data = bytes_data

    # Return the converted data
    return converted_data

  def write_structure(self, name:str, df:pd.DataFrame):
    """
    Writes a dataframe back to this instances [data] using the specification 
    provided in [structures].

    Arguments:
      name (str): The name of the structure to write.
      df (pd.DataFrame): The dataframe to write.
    """
     # Assert that structure exists.
    assert self.__structures is not None, "There are no structures defined."
    assert name in self.__structures, f"Structure with name '{name}' does not "\
      + "exist. Add it using [add_structure] before writing to it."

    # Get the structure
    structure = self.__structures[name]

    # Check that the column names of the dataframe matches the variable names.
    for i in range(len(df.columns)):
      assert df.columns[i] == structure.variables[i].name, \
        f"Structure name '{structure.variables[i].name}' does not match " \
        + f"DataFrame column name 'df.columns[i]'."

    # Check that number of rows matches [structure.rows]
    assert df.shape[0] == structure.rows, \
      f"Number of rows in DataFrame ({df.shape[0]}) does not match number of "\
        + f"rows in structure ({structure.rows})."

    # Iterate the rows of the dataframe saving its contents to [data]
    for row in range(structure.rows):
      row_data = df.iloc[row]

      for var in structure.variables:
        # Calculate the offset as the offset of the row + the offset of the
        # variable.
        offset = int(row * len(structure) / structure.rows)

        # Get the data
        item = row_data[var.name]

        # Write the variable
        self.write_variable(item, var, offset)
        
  def write_variable(self, data:object, variable:Variable, offset:int=None):
    """
    Writes a variable to the data, converts it back to bytes.

    Arguments:
      data (object): The data to write.
      variable (Variable): The definition of the variable to write.
      offset (int, optional): Offset to apply. Added to variable offset. Used
        to write repeating structures. If not specified, then no offset is 
        applied.
    """
    # Convert to native types.
    if isinstance(data, np.integer):
      data = int(data)
    elif type(data) in [bool, np.bool_]:
      data = bool(data)
    elif isinstance(data, str):
      data = str(data)
    elif isinstance(data, float):
      data = float(data)
      
    # Confirm that the provided data type matches the type specified in the
    # [variable].
    assert type(data) == variable.datatype, \
      f"Datatype {type(data)} is not a subtype of {variable.datatype}"

    # Calculate the full offset. Any offset passed to this method + the 
    # variable offset.
    full_offset = variable.offset if offset is None else variable.offset \
        + offset
    
    # Check the bounds
    self.__check_bounds(full_offset, variable.size)

     # Write the data.
    if variable.datatype == str:
      self.__write(full_offset, data.encode(self.__str_encode))
    elif variable.datatype in [int, bool]:
      self.__write(full_offset,
                   data.to_bytes(variable.size,
                                 byteorder=variable.byteorder.value,
                                 signed=variable.signed))
    elif variable.datatype == float:
      endian_sign = '<' if variable.byteorder == ByteOrder.LITTLE else '>'
      self.__write(full_offset, struct.pack(f'{endian_sign}f', data))
    else:
      self.__write(full_offset, data)

  def __check_bounds(self, offset:int, length:int):
    """
    Checks that the offset and length is within the bounds of the data.

     Arguments:
      offset (int): The start position to test.
      length: The number of bytes to test.
    """
    assert offset < len(self.data), f"Offset {offset} is out of bounds for "\
      + f"data of length {len(self.data)}."
    
    assert offset + length <= len(self.data), f"Length {length} is out of "\
      + f"bounds for data length {len(self.data)} starting at {offset}."
    

  def __read(self, offset:int, length:int) -> bytes:
    """
    Gets the bytes from [data] at offset.

    Arguments:
      offset (int): The position of the data to read. The byte at offset
        position and [length] following bytes will be returned.
      length: The number of bytes to return.

    Returns:
      bytes: The [length] bytes starting at [offset]
    """
    self.__check_bounds(offset, length)
    return self.__data[offset:offset+length]


  def __write(self, offset:int, value:bytes):
    """
    Writes [value] to [data] at position [offset].

    Arguments:
      offset (int): The position of the data to update. The byte at offset
        position and any following bytes up to the length of [value] will be
        updated.
      value: The value to write.
    """
    self.__check_bounds(offset, len(value))
    self.__data = self.__data[:offset] + value \
        + self.__data[offset+len(value):]
