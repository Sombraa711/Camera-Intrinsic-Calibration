import os
import sys
import argparse
import numpy as np
import pycolmap
import cv2

class CameraCalibrator:

    def __init__(self, source):
        self.intrinsic_matrix = None
        
        if os.path.isdir(source) == False:
            try:
                print(f"Try using camera {source} to calculate camera parameters")
                cap = cv2.VideoCapture(int(source))
                if cap is None or not cap.isOpened():
                    print('Warning: unable to open video source: ', source)
                    exit(0)
                os.makedirs(os.path.join(os.path.dirname(os.path.realpath(__file__)), f'camera{source}'), exist_ok = True)
                self.image_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), f'camera{source}')
                frame_id = 0
                while True:
                    ret, frame = cap.read()
                    if ret == False:
                        break
                    cv2.imwrite(os.path.join(self.image_dir, f"{str(frame_id).zfill(7)}.png"), frame)     # save frame as PNG file
                    frame_id += 1
                    if frame_id >= 100:
                        break
                cap.release()
                print(f"{frame_id} Frames Saved In {self.image_dir}")
            except Exception as e:
                print(f"Error: {e}")
        else:
            self.image_dir = source


    def camera_parameter_generate(
            self,
            camera_model = "PINHOLE",
    ):
        '''
        Sombra: 'virtual' stands for: We actually do not need this. but the wrapper of pycolmap contains it,
        and there is no smaller unit for skipping writting to .db filem.
        '''
        virtual_database_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'virtual_database.db')
        '''
        /* PIPELINE */
        m.def("extract_features",
                &ExtractFeatures,
                "database_path"_a,
                "image_path"_a,
                "image_list"_a = std::vector<std::string>(),
                "camera_mode"_a = CameraMode::AUTO,
                "camera_model"_a = "SIMPLE_RADIAL",
                "reader_options"_a = ImageReaderOptions(),
                "sift_options"_a = sift_extraction_options,
                "device"_a = Device::AUTO,
                "Extract SIFT Features and write them to database");
        }
        '''
        pycolmap.extract_features(virtual_database_path, self.image_dir, camera_model = camera_model)
        # cameras = pycolmap.Database(virtual_database_path).read_all_cameras()
        # cameras[-1].calibration_matrix()
        self.intrinsic_matrix = pycolmap.Database(virtual_database_path).read_camera(1).calibration_matrix()
        return self.intrinsic_matrix

    def export_intrinsic_matrix(self):
        target_write_path = os.path.join(os.path.dirname(self.image_dir), 'cam_K.txt')
        if os.path.exists(target_write_path):
            print(f"{target_write_path} exists. Pls CHECK it.")
            return
        np.savetxt(target_write_path, self.intrinsic_matrix)
        print(f"cam_K.txt Saved In {target_write_path} ")
        return

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=str, required = True)
    args = parser.parse_args()

    camera_calibrator = CameraCalibrator(args.source)
    camera_calibrator.camera_parameter_generate()
    camera_calibrator.export_intrinsic_matrix()
