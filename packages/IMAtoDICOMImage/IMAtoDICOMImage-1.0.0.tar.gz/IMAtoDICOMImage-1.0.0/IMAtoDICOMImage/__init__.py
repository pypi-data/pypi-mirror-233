import pydicom
from pydicom.dataset import Dataset, FileDataset
from pydicom.uid import ExplicitVRLittleEndian
import pydicom._storage_sopclass_uids
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import imageio

class IMAConverter:
    #this lib ganna use to convert a .IMA file (medical image) to a DICOM (.dcm) file or "image"
    
    def __init__(self , ima_file_path):
        self.ima_file_path = ima_file_path
        
        
    def converter_ImaToDicom(self, dicom_file_path, all_frames=False , frame_index=0 ):
        
        # Load the IMA file
        dcm_dataset = pydicom.dcmread(self.ima_file_path)
        
        # Extract the pixel data from the IMA file
        pixel_data = dcm_dataset.pixel_array
        
        
        # Select the frame you want to export (e.g., frame index 0) 
        if dcm_dataset.NumberOfFrames==1:
            frame_data = pixel_data
        else:
            if all_frames==True:
                frame_data = pixel_data
            else:
                frame_data = pixel_data[frame_index]
            
        
        
        # Create a new DICOM dataset for the exported frame (encoding)
        meta = pydicom.Dataset()
        meta.MediaStorageSOPClassUID = pydicom._storage_sopclass_uids.RTImageStorage
        meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
        meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
        
        ds = Dataset()
        ds.file_meta = meta
        ds.is_little_endian = True
        ds.is_implicit_VR = False
        ds.SOPClassUID = pydicom._storage_sopclass_uids.RTImageStorage
        
        # Copy the metadata from the original IMA file to the exported DICOM dataset
        ds.update(dcm_dataset)
        pydicom.dataset.validate_file_meta(ds.file_meta, enforce_standard=True)
        
        
        # Update the pixel data with the exported frame
        ds.PixelData = frame_data.tobytes()
        if all_frames==False:
            ds.NumberOfFrames = 1
        else:
            pass
        
        # Save the exported DICOM file
        ds.save_as(dicom_file_path)
        print("dicom file saved")
        
#---------------------------------------------------------------------
    def show_IMA_ImageFrame(self,frame_index=0):
        
        #you can use this function to show your IMA file image frames
        dcm_dataset = pydicom.dcmread(self.ima_file_path)
        
        if dcm_dataset.NumberOfFrames!=1:
            print("IMA file have multiple frames")
            plt.imshow(dcm_dataset.pixel_array[frame_index], cmap='gray')
            plt.axis('off')  # Turn off the axis labels
            plt.show()
        else:
            plt.imshow(dcm_dataset.pixel_array, cmap='gray')
            plt.axis('off')  # Turn off the axis labels
            plt.show()
#-------------------------------------------------------------------------
    def IMA_MetaData_ToDict(self):
        dcm_dataset = pydicom.dcmread(self.ima_file_path)
        dicom_dict = dict(dcm_dataset)
        return dicom_dict
        
#----------------------------------------------------------------------  
    def IMA_to_jpg(self,jpg_file_path ,frame_index=0):
        dcm_dataset = pydicom.dcmread(self.ima_file_path)
        
        if dcm_dataset.NumberOfFrames==1:
            frame=dcm_dataset.pixel_array
        else:
            frame=dcm_dataset.pixel_array[frame_index]
            
        image_array = np.array(frame, dtype=np.uint16)
        image = Image.fromarray(image_array)

        # Save the image as a JPEG file
        image.save(jpg_file_path)
        
        print("file saved in:",jpg_file_path)
#---------------------------------------------------------------------
    def IMA_to_png(self,png_file_path ,frame_index=0):
        dcm_dataset = pydicom.dcmread(self.ima_file_path)
        
        if dcm_dataset.NumberOfFrames==1:
            frame=dcm_dataset.pixel_array
        else:
            frame=dcm_dataset.pixel_array[frame_index]
            
        image_array = np.array(frame)
        image = Image.fromarray(image_array)

        # Save the image as a PNG file
        image.save(png_file_path)
        print("file saved in:",png_file_path)
#---------------------------------------------------------------------
    def IMA_to_tif(self, tif_file_path ,frame_index=0):
        dcm_dataset = pydicom.dcmread(self.ima_file_path)
        
        if dcm_dataset.NumberOfFrames==1:
            frame=dcm_dataset.pixel_array
        else:
            frame=dcm_dataset.pixel_array[frame_index]
            
        image_array = np.array(frame)

        # Save the array as a TIFF image
        imageio.imwrite(tif_file_path, image_array)
        print("file saved in:",tif_file_path)
