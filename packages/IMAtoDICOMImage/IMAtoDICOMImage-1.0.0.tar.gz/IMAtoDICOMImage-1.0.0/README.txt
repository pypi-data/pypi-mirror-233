# IMA to DICOM/Image Converter

The IMA to DICOM/Image Converter is a Python library designed to convert .IMA files, typically used for medical images, into DICOM (.dcm) files or various image formats such as JPEG, PNG, and TIFF. This library is especially useful when dealing with medical imaging data and the need to convert it into different formats for analysis or visualization.

## Installation

You can install the IMA to DICOM/Image Converter using pip:

```bash
pip install IMAtoDICOMImage

Usage:
To use this library, you can follow these basic steps:

Import the required modules and classes:

from IMAtoDICOMImageConverter import IMAConverter

Create an instance of the IMAConverter class, providing the path to your .IMA file:

ima_converter = IMAConverter("path/to/your/file.ima")


Convert .IMA to DICOM:

ima_converter.converter_ImaToDicom("path/to/save/dicom.dcm")


Convert .IMA to other image formats (JPEG, PNG, TIFF):

ima_converter.IMA_to_jpg("path/to/save/image.jpg")
ima_converter.IMA_to_png("path/to/save/image.png")
ima_converter.IMA_to_tif("path/to/save/image.tif")


Display .IMA image frames:

ima_converter.show_IMA_ImageFrame()

Extract metadata to a dictionary:

metadata = ima_converter.IMA_MetaData_ToDict()

Examples
Here are some examples of how to use this library:


# Convert .IMA to DICOM
ima_converter.converter_ImaToDicom("output.dcm")

# Convert .IMA to JPEG
ima_converter.IMA_to_jpg("output.jpg")

# Display .IMA image frame
ima_converter.show_IMA_ImageFrame()

# Extract metadata to a dictionary
metadata = ima_converter.IMA_MetaData_ToDict()


Requirements:
Python 3.x
pydicom
numpy
matplotlib
pillow (PIL)
imageio
License

This library is released under the MIT License. See the LICENSE file for details.

Credits
This library was developed by Maryam Oghbaei and is open-source to support the medical imaging community.

If you have any questions or encounter issues, please feel free to ask by email:
maryam.oghbayi@gmail.com

Happy coding!

