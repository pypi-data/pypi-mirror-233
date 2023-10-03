import base64
import cv2
import io
import numpy as np
import re
from datetime import datetime
from PIL import Image
from skimage.transform import radon
from google.cloud import vision_v1
from pkg_resources import resource_filename
from idvpackage.ocr_utils import *
import face_recognition
import tempfile
from googletrans import Translator
from PIL import Image, ImageEnhance
import json

class IdentityVerification:

    def __init__(self):
        """
        This is the initialization function of a class that imports a spoof model and loads an OCR
        reader.
        """
        #self.images = images
        credentials_path = resource_filename('idvpackage', 'streamlit-connection-b1a38b694505.json')
        #credentials_path = "streamlit-connection-b1a38b694505.json"
        self.client = vision_v1.ImageAnnotatorClient.from_service_account_json(credentials_path)
        
    def image_conversion(self,image):  
        """
        This function decodes a base64 string data and returns an image object.
        :return: an Image object that has been created from a base64 encoded string.
        """
        # image=image.split(',')[-1]
        # Decode base64 String Data
        img=Image.open(io.BytesIO(base64.decodebytes(bytes(image, "utf-8"))))
        return img

    def rgb2yuv(self, img):
        """
        Convert an RGB image to YUV format.
        """
        try:
            img=np.array(img)
            return cv2.cvtColor(img, cv2.COLOR_RGB2YUV)
        except Exception as e:
            raise Exception(f"Error: {e}")
    
    def find_bright_areas(self, image, brightness_threshold):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh_image = cv2.threshold(gray_image, brightness_threshold, 255, cv2.THRESH_BINARY)[1]
        contours, hierarchy = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        bright_areas = []

        for contour in contours:
            bounding_box = cv2.boundingRect(contour)

            area = bounding_box[2] * bounding_box[3]

            if area > 800:
                bright_areas.append(bounding_box)

        return len(bright_areas)

    def is_blurry(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        laplacian_variance = cv2.Laplacian(gray_image, cv2.CV_64F).var()
        
        return laplacian_variance

    def identify_input_type(self, data):
        if isinstance(data, bytes):
                return "video_bytes"
        else:
            pass

        try:
            decoded_data = base64.b64decode(data)
            
            if decoded_data:
                return "base_64"
        except Exception:
            pass

        return "unknown"

    def sharpen_image(self, image):
        kernel = np.array([[-1, -1, -1],
                        [-1, 9, -1],
                        [-1, -1, -1]])
        return cv2.filter2D(image, -1, kernel)


    def adjust_contrast(self, image, factor):
        pil_image = Image.fromarray(image)
        enhancer = ImageEnhance.Contrast(pil_image)
        enhanced_image = enhancer.enhance(factor)
        return np.array(enhanced_image)

    def adjust_brightness(self, image, factor):
        pil_image = Image.fromarray(image)
        enhancer = ImageEnhance.Brightness(pil_image)
        enhanced_image = enhancer.enhance(factor)
        return np.array(enhanced_image)

    def enhance_quality(self, image):
        sharpened_image = self.sharpen_image(image)
        enhanced_image = self.adjust_brightness(sharpened_image, 1.2)
        enhanced_contrast = self.adjust_contrast(enhanced_image, 1.2)
        # grayscale_image = cv2.cvtColor(enhanced_contrast, cv2.COLOR_BGR2GRAY)
        
        return enhanced_contrast
    
    def check_document_quality(self, data, brightness_threshold=230, blur_threshold=3500, video_duration_threshold=3):
        input_type = self.identify_input_type(data)
        if input_type == 'base_64':
            image_quality = {
                'error': ''
            }
            
            try:
                # Check if the image can be converted from RGB to YUV
                enhanced_data = self.enhance_quality(np.array(self.image_conversion(data)))
                yuv_img = self.rgb2yuv(self.image_conversion(data))

            except:
                # print("yuv error")
                image_quality['error'] = 'bad_image'

            try:
                # Check brightness
                brightness = np.average(enhanced_data[..., 0])
                # print(f"brightness: {brightness}")
                if brightness > brightness_threshold:
                    # print(f"bright, {brightness}")
                    image_quality['error'] = 'bad_image'
            except:
                # print("bright")
                image_quality['error'] = 'bad_image'

            try:
                # Check blurriness
                # image = np.array(self.image_conversion(data))
                gray = cv2.cvtColor(enhanced_data, cv2.COLOR_BGR2GRAY)
                fm = cv2.Laplacian(gray, cv2.CV_64F).var()
                # print(f"blurr: {fm}")
                if fm < blur_threshold:
                    # print(f"blur, {fm}")
                    image_quality['error'] = 'bad_image'
            except:
                # print("blur")
                image_quality['error'] = 'bad_image'
            
            try:
                # check image coloured or gray
                if not self.is_colored(data):
                    image_quality['error'] = 'bad_image'
            except:
                image_quality['error'] = 'bad_image'
            
            return image_quality
        
        elif input_type == 'video_bytes':
            video_quality = {
                'error': ''
            }
            frame_count_vid = 0
            try:
                with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
                    temp_video_file.write(data)
                
                video_capture = cv2.VideoCapture(temp_video_file.name)

                if video_capture.isOpened():
                    fps = int(video_capture.get(cv2.CAP_PROP_FPS))
                    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = frame_count / fps
                    # print(f"duration: {duration} seconds")
                    if duration < video_duration_threshold:  # Assuming a threshold of 3 seconds
                        video_quality['error'] = 'bad_video'

                    for _ in range(frame_count):
                        ret, frame = video_capture.read()
                        if ret:
                            frame_count_vid+=1
                            if frame_count_vid % 10 == 0:
                                _, buffer = cv2.imencode('.jpg', frame)
                                image_data = buffer.tobytes()

                                image = vision_v1.Image(content=image_data)

                                response = self.client.face_detection(image=image)
                                if len(response.face_annotations) >= 1:
                                    # Face detected in at least one frame
                                    break
                    else:
                        # No face detected in any frame
                        video_quality['error'] = 'bad_video'

            except Exception:
                video_quality['error'] = 'bad_video'

            return video_quality

    # def check_image_quality(self, id_card, brightness_threshold=245, blur_threshold=150):
    #     id_card = self.image_conversion(id_card)
    #     id_card = np.array(id_card)
    #     bright_result = self.find_bright_areas(id_card, brightness_threshold)
    #     blurry_result = self.is_blurry(id_card)

    #     if bright_result > 1:
    #         raise Exception(f"Image is too bright. Threshold: {brightness_threshold}")

    #     if blurry_result < blur_threshold:
    #         raise Exception(f"Image is too blurry. Blurriness: {blurry_result}, Threshold: {blur_threshold}")

    def process_image(self,front_id):
        img = self.image_conversion(front_id)
        img = np.array(img)
        I = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        h, w = I.shape
        if (w > 640):
            I = cv2.resize(I, (640, int((h / w) * 640)))
        I = I - np.mean(I)
        sinogram = radon(I)
        r = np.array([np.sqrt(np.mean(np.abs(line) ** 2)) for line in sinogram.transpose()])
        rotation = np.argmax(r)
        angle = round(abs(90 - rotation)+0.5)

        if abs(angle) > 5:
            color_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            im = Image.fromarray(color_img)
            out = im.rotate(angle, expand=True)
        else:
            out = Image.fromarray(img)
    
        # im = self.image_conversion(front_id)
        # out = im.rotate(angle, expand=True)

        return out

    def is_colored(self, base64_image):
        img = self.image_conversion(base64_image)
        img = np.array(img)

        return len(img.shape) == 3 and img.shape[2] >= 3
    
    def get_blurred_and_glared_for_doc(self, image, brightness_threshold=230, blur_threshold=3500):
        blurred = 'clear'
        glare = 'clear'
        
        # image = self.image_conversion(image)
        # image_arr = np.array(image)
        enhanced_data = self.enhance_quality(image)

        blurry1 = self.is_blurry(enhanced_data)

        if blurry1 < blur_threshold:
            blurred = 'consider'
        
        # yuv_image = self.rgb2yuv(image)
        brightness1 = np.average(enhanced_data[..., 0])
        if brightness1 > brightness_threshold:
            glare = 'consider'

        # glare1 = self.find_bright_areas(front_id_arr, 245)
        # glare2 = self.find_bright_areas(back_id_arr, 245)
        # if glare1 > 5 or glare2 > 5:
        #     glare = 'consider'
        
        return blurred, glare

    def get_face_orientation(self, face_landmarks):
        left_eye = np.array(face_landmarks['left_eye']).mean(axis=0)
        right_eye = np.array(face_landmarks['right_eye']).mean(axis=0)

        eye_slope = (right_eye[1] - left_eye[1]) / (right_eye[0] - left_eye[0])
        angle = np.degrees(np.arctan(eye_slope))

        return angle

    def extract_selfie_from_video(self, video_bytes):
        video_dict = {
            'error': ''
        }

        with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
            temp_video_file.write(video_bytes)
        
        cap = cv2.VideoCapture(temp_video_file.name)

        # Initialize variables to keep track of the best frame and face score
        best_frame = None
        best_score = 0

        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            
            if frame_count % 3 != 0:
                continue
                
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(rgb_frame)
            face_landmarks_list = face_recognition.face_landmarks(rgb_frame)

            face_score = len(face_locations)

            for landmarks in face_landmarks_list:
                angle = self.get_face_orientation(landmarks)
                # print(f"Current angle: {angle}")
                if abs(angle) < 1:
                    if face_score > best_score:
                        best_score = face_score
                        best_frame = frame.copy()

        cap.release()

        if best_frame is not None:
            return best_frame
        else:
            video_dict['error'] = 'bad_video'

    def load_and_process_image_fr(self, base64_image, arr=False):
        try:
            if not arr:
                img = self.process_image(base64_image)
                img = np.array(img)
                image = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            else:
                image = cv2.cvtColor(base64_image, cv2.COLOR_RGB2BGR)

            # base64_image = base64_image.split(',')[-1]
            # image_data = base64.b64decode(base64_image)
            # image_file = io.BytesIO(image_data)

            # image = face_recognition.load_image_file(image_file)

            face_locations = face_recognition.face_locations(image)

            if not face_locations:
                return [], []
        
            face_encodings = face_recognition.face_encodings(image, face_locations)

            return face_locations, face_encodings
        except:
            return [], []
        
    def calculate_similarity(self, face_encoding1, face_encoding2):
        similarity_score = 1 - face_recognition.face_distance([face_encoding1], face_encoding2)[0]
        return round(similarity_score + 0.25, 2)

    def extract_face_and_compute_similarity(self, selfie, front_face_locations, front_face_encodings):
        face_locations1, face_encodings1 = self.load_and_process_image_fr(selfie, arr=True)
        face_locations2, face_encodings2 = front_face_locations, front_face_encodings

        if not face_encodings1 or not face_encodings2.any():
            return 0
        else:
            # face_encoding1 = face_encodings1[0]
            # face_encoding2 = face_encodings2[0]
            largest_face_index1 = face_locations1.index(max(face_locations1, key=lambda loc: (loc[2] - loc[0]) * (loc[3] - loc[1])))
            largest_face_index2 = face_locations2.index(max(face_locations2, key=lambda loc: (loc[2] - loc[0]) * (loc[3] - loc[1])))

            face_encoding1 = face_encodings1[largest_face_index1]
            face_encoding2 = face_encodings2[largest_face_index2]

            similarity_score = self.calculate_similarity(face_encoding1, face_encoding2)

            return min(1, similarity_score)
    
    def calculate_landmarks_movement(self, current_landmarks, previous_landmarks):
        return sum(
            abs(cur_point.position.x - prev_point.position.x) +
            abs(cur_point.position.y - prev_point.position.y)
            for cur_point, prev_point in zip(current_landmarks, previous_landmarks)
        )

    def calculate_face_movement(self, current_face, previous_face):
        return abs(current_face[0].x - previous_face[0].x) + abs(current_face[0].y - previous_face[0].y)

    def calculate_liveness_result(self, eyebrow_movement, nose_movement, lip_movement, face_movement):
        eyebrow_movement_threshold = 15.0
        nose_movement_threshold = 15.0
        lip_movement_threshold = 15.0
        face_movement_threshold = 10.0

        if (
            eyebrow_movement > eyebrow_movement_threshold or
            nose_movement > nose_movement_threshold or
            lip_movement > lip_movement_threshold or
            face_movement > face_movement_threshold
        ):
            return True
        else:
            return False

    def check_for_liveness(self, similarity, video_bytes):
        # cap = cv2.VideoCapture(video)
        with tempfile.NamedTemporaryFile(delete=False) as temp_video_file:
            temp_video_file.write(video_bytes)
        
        cap = cv2.VideoCapture(temp_video_file.name)

        frame_count = 0
        previous_landmarks = None
        previous_face = None
        liveness_result_list = []

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1

            if frame_count % 10 == 0:  # analyze every 10 frames
                _, buffer = cv2.imencode('.jpg', frame)
                image_data = buffer.tobytes()

                image = vision_v1.Image(content=image_data)

                response = self.client.face_detection(image=image)
                faces = response.face_annotations

                largest_face = None
                largest_face_area = 0

                for face in faces:
                    current_landmarks = face.landmarks
                    current_face = face.bounding_poly.vertices
                    face_area = abs((current_face[2].x - current_face[0].x) * (current_face[2].y - current_face[0].y))

                    if face_area > largest_face_area:
                        largest_face = face
                        largest_face_area = face_area

                if largest_face:
                    # face = faces[0]
                    current_landmarks = largest_face.landmarks
                    current_face = largest_face.bounding_poly.vertices

                    if previous_landmarks and previous_face:
                        eyebrow_movement = self.calculate_landmarks_movement(current_landmarks[:10], previous_landmarks[:10])

                        nose_movement = self.calculate_landmarks_movement(current_landmarks[10:20], previous_landmarks[10:20])

                        lip_movement = self.calculate_landmarks_movement(current_landmarks[20:28], previous_landmarks[20:28])

                        face_movement = self.calculate_face_movement(current_face, previous_face)

                        liveness_result = self.calculate_liveness_result(eyebrow_movement, nose_movement, lip_movement, face_movement)

                        liveness_result_list.append(liveness_result)

                    previous_landmarks = current_landmarks
                    previous_face = current_face

        cap.release()

        if any(liveness_result_list) and similarity>=0.60:
            liveness_check_result = 'clear'
        else:
            liveness_check_result = 'consider'

        return liveness_check_result

    def extract_id_number_from_front_id(self, front_id_text):
        try:
            id_number_match = re.search(r'.*ID Number\n*([\d-]+)', front_id_text)
            if id_number_match:
                id_number = id_number_match.group(1).replace('-','')
            else:
                id_number = ''
        except:
            id_number = ''

        return id_number
    
    def extract_name_from_front_id(self, front_id_text):
        try:
            name_match = re.search(r'Name: (.+)', front_id_text)
            if name_match:
                name = name_match.group(1)
            else:
                name = ''
        except:
            name = ''

        return name
    
    def extract_dob_from_fron_id(self, front_id_text):
        try:
            date_matches = re.findall(r'(\d{2}/\d{2}/\d{4})', front_id_text)
            date_objects = [datetime.strptime(date, '%d/%m/%Y') for date in date_matches]
            date_of_birth = min(date_objects).strftime('%d/%m/%Y')
        except:
            date_of_birth = ''
        
        return date_of_birth
    
    def extract_expiry_date_from_fron_id(self, front_id_text):
        try:
            date_matches = re.findall(r'(\d{2}/\d{2}/\d{4})', front_id_text)
            date_objects = [datetime.strptime(date, '%d/%m/%Y') for date in date_matches]
            expiry_date = max(date_objects).strftime('%d/%m/%Y')
        except:
            expiry_date = ''
        
        return expiry_date

    def get_ocr_results(self, processed_image):
        with io.BytesIO() as output:
            processed_image.save(output, format="PNG")
            image_data = output.getvalue()

        image = vision_v1.types.Image(content=image_data)
        response = self.client.text_detection(image=image)
        id_infos = response.text_annotations

        return id_infos
    
    def extract_document_info(self, image, document_type, side, country='UAE', nationality='Russia'):
        document_data = {}
        if document_type == 'national_id' and country=='UAE':
            # print(f"getting fron data")
            if side=='front':
                document_data = self.extract_front_id_info(image, country)

            if side=='back':
                document_data = self.extract_back_id_info(image, country)

        if document_type == 'passport' and country=='UAE':
            document_data = self.exract_passport_info(image, nationality)
        
        return document_data
        
    def extract_front_id_info(self, front_id, country='UAE'):
        if country == 'UAE':
            front_data = {
                'error': ''
            }
            is_colored1 = self.is_colored(front_id)
            if is_colored1:
                try:
                    processed_front_id = self.process_image(front_id)
                    front_id_text = self.get_ocr_results(processed_front_id)
                    front_id_text = front_id_text[0].description

                    if identify_front_id(front_id_text):
                        id_number = self.extract_id_number_from_front_id(front_id_text)
                        dob = self.extract_dob_from_fron_id(front_id_text)
                        expiry_date = self.extract_expiry_date_from_fron_id(front_id_text)
                        name = self.extract_name_from_front_id(front_id_text)

                        img = self.image_conversion(front_id)
                        image = np.array(img)
                        pil_image = Image.fromarray(image)

                        doc_on_pp_result = document_on_printed_paper(image)

                        with io.BytesIO() as output:
                            pil_image.save(output, format="PNG")
                            image_data = output.getvalue()

                        logo_result = detect_logo(self.client, image_data)
                        screenshot_result = detect_screenshot(self.client, front_id)
                        photo_on_screen_result = detect_photo_on_screen(self.client, front_id)

                        front_blurred, front_glare = self.get_blurred_and_glared_for_doc(image)

                        front_face_locations, front_face_encodings = self.load_and_process_image_fr(front_id)

                        front_face_locations_str = json.dumps([tuple(face_loc) for face_loc in front_face_locations])
                        front_face_encodings_str = json.dumps([face_enc.tolist() for face_enc in front_face_encodings])

                        front_data = {
                            'front_extracted_data': front_id_text,
                            'front_coloured': True,
                            'front_id_number': id_number,
                            'front_dob': dob,
                            'front_expiry_date': expiry_date,
                            'front_name': name,
                            'front_doc_on_pp': doc_on_pp_result,
                            'front_logo_result': logo_result,
                            'front_screenshot_result': screenshot_result,
                            'front_photo_on_screen_result': photo_on_screen_result,
                            'front_blurred': front_blurred, 
                            'front_glare': front_glare,
                            'front_face_locations': front_face_locations_str, 
                            'front_face_encodings': front_face_encodings_str
                        }

                        non_optional_keys = ["front_id_number", "front_name"]
                        empty_string_keys = [key for key, value in front_data.items() if key not in non_optional_keys and value == '']

                        if empty_string_keys:
                            front_data['error'] = 'covered_photo'
                    else:
                        front_data['error'] = 'not_front_id'

                except Exception as e:
                    print(e)
                    front_data['error'] = 'bad_image'
                
            else:
                front_data['error'] = 'bad_image'
            
            return front_data
    
    def extract_back_id_info(self, back_id, country='UAE'):
        if country=='UAE':
            back_data = {
                'error': ''
            }
            is_colored2 = self.is_colored(back_id)
            if is_colored2:
                try:
                    processed_back_id = self.process_image(back_id)
                    id_infos= self.get_ocr_results(processed_back_id)
                    text = id_infos[0].description

                    if identify_back_id(text):
                        id_number_pattern = r'(?:ILARE|IDARE)\s*([\d\s]+)'
                        #card_number_pattern = r'(?:\b|Card Number\s*/\s*رقم البطاقة\s*)\d{9}(?:\b|\s*)'
                        card_number_pattern = r'(\b\d{9}\b)|\b\w+(\d{9})\b|Card Number\s*(\d+)|Card Number\s*/\s*رقم البطاقة\s*(\d+)'
                        date_pattern = r'(\d{2}/\d{2}/\d{4})'
                        #(\d{2}/\d{2}/\d{4}) Date of Birth|\n
                        #expiry_date_pattern = r'\n(\d{2}/\d{2}/\d{4})\s*\n'
                        gender_pattern = r'Sex: ([A-Z])|Sex ([A-Z])'
                        nationality_pattern = r'([A-Z]+)<<'
                        # name_pattern = r'([A-Z]+(?:<<[A-Z]+)+(?:<[A-Z]+)+(?:<[A-Z]+))|([A-Z]+(?:<<[A-Z]+)+(?:<[A-Z]+))|([A-Z]+(?:<[A-Z]+)+(?:<<[A-Z]+)+(?:<[A-Z]+)+)'
                        name_pattern = r'(.*[A-Za-z]+<[<]+[A-Za-z].*)'
                        occupation_pattern = r'Occupation:\s*([\w\s.]+)'
                        employer_pattern = r'Employer:\s*([\w\s.]+)'
                        issuing_place_pattern = r'Issuing Place:\s*([\w\s.]+)'
                        # mrz_pattern = r'(ILARE.*|IDARE.*)'
                        mrz_pattern = r'(ILARE.*\n*.*\n*.*\n*.*|IDARE.*\n*.*\n*.*\n*.*)'

                        try:
                            id_number = re.search(id_number_pattern, text)
                            id_number = id_number.group(0).replace(" ", "")[15:30]
                        except:
                            id_number = ''
                        
                        try:
                            card_number = re.findall(card_number_pattern, text)
                            card_number = [c for c in card_number if any(c)]
                            if card_number:
                                card_number = "".join(card_number[0])
                        except:
                            card_number = ''
                        
                        dob, expiry_date = '', ''
                        
                        dates = re.findall(date_pattern, text)
                        sorted_dates = sorted(dates, key=lambda x: datetime.strptime(x, '%d/%m/%Y'))

                        date = [d for d in sorted_dates if any(d)]
                        if date:
                            try:
                                dob = "".join(date[0])
                            except:
                                dob = ''
                            try:
                                expiry_date = "".join(date[1])
                            except:
                                expiry_date = ''

                        #expiry_date = re.search(expiry_date_pattern, text)
                        
                        gender = re.findall(gender_pattern, text)
                        if gender:
                            gender = "".join(gender[0])
                        if not gender:
                            gender_pattern = r'(?<=\d)[A-Z](?=\d)'
                            gender = re.search(gender_pattern, text)
                            gender = gender.group(0) if gender else ''
                            
                        try:
                            nationality = re.search(nationality_pattern, text)
                            nationality = nationality.group(1)
                        except:
                            nationality = ''
                        
                        try:
                            name = re.findall(name_pattern, text)
                            name = [n for n in name if any(n)]
                            if name:
                                name = "".join(name[0])
                                name = name.replace('<',' ').strip()
                        except:
                            name = ''
                        
                        try:
                            occupation = re.search(occupation_pattern, text, re.IGNORECASE)
                            occupation = occupation.group(1).strip().split('\n', 1)[0]
                        except:
                            occupation = ''
                        
                        try:
                            employer = re.search(employer_pattern, text, re.IGNORECASE)
                            employer = employer.group(1).strip().split('\n', 1)[0]
                        except:
                            employer = ''
                                
                        try:
                            issuing_place = re.search(issuing_place_pattern, text, re.IGNORECASE)
                            issuing_place = issuing_place.group(1).strip().split('\n', 1)[0]
                        except:
                            issuing_place = ''
                        
                        try:
                            mrz = re.findall(mrz_pattern, text, re.MULTILINE)
                            input_str = mrz[0].replace(" ", "")
                            mrz1, remaining = input_str.split("\n", 1)
                            mrz2, mrz3 = remaining.rsplit("\n", 1)
                        # mrz1, mrz2, mrz3 = mrz[0].replace(' ','')mrz.split("\n")
                        except:
                            mrz, mrz1, mrz2, mrz3 = '', '', '', ''
                        
                        if is_valid_and_not_expired(expiry_date) == 'consider':
                            back_data['error'] = 'expired_document'

                        img = self.image_conversion(back_id)
                        image = np.array(img)
                        pil_image = Image.fromarray(image)
                        
                        doc_on_pp_result = document_on_printed_paper(image)
                        screenshot_result = detect_screenshot(self.client, back_id)
                        photo_on_screen_result = detect_photo_on_screen(self.client, back_id)
                        back_blurred, back_glare = self.get_blurred_and_glared_for_doc(image)

                        back_data = {
                            'back_extracted_data': text,
                            'back_coloured': True,
                            'id_number': id_number,
                            'card_number': card_number,
                            'name': name,
                            'dob': dob ,
                            'expiry_date': expiry_date,
                            'gender': gender,
                            'nationality': nationality,
                            'occupation': occupation,
                            'employer': employer,
                            'issuing_place': issuing_place,
                            'mrz': mrz,
                            'mrz1': mrz1,
                            'mrz2': mrz2,
                            'mrz3': mrz3,
                            'doc_on_pp': doc_on_pp_result,
                            'screenshot_result': screenshot_result,
                            'photo_on_screen_result': photo_on_screen_result,
                            'back_blurred': back_blurred, 
                            'back_glare': back_glare
                        }

                        non_optional_keys = ["id_number", "card_number", "name", "dob", "expiry_date", "gender", "nationality", "mrz", "mrz1", "mrz2", "mrz3", "similarity"]
                        empty_string_keys = [key for key, value in back_data.items() if key not in non_optional_keys and value == '']

                        if empty_string_keys:
                            back_data['error'] = 'covered_photo'

                    else:
                        back_data['error'] = 'bad_image'
                except:
                    back_data['error'] = 'bad_image'

            else:
                back_data['error'] = 'bad_image'

            return back_data

    def exract_passport_info(self, passport, nationality='Russia'):
        if nationality == 'Russia':
            processed_passport = self.process_image(passport)
            passport_text = self.get_ocr_results(processed_passport)
            passport_text = passport_text[0].description

            passport_details = {}

            passport_number_pattern = r"(\d{7})"
            # date_of_birth_pattern = r"Дата рождения/Date of birth\n(.*?)\n"
            # date_of_issue_pattern = r"Дата выдачи/Date of issue\n(.*?)\n"
            # date_of_expiry_pattern = r"Дата окончания сроки Date of expiry\.\n.*?\n(.*?)\n"
            date_pattern = r"\b(\d{2}\.\d{2}\.\d{4})\b"
            surname_pattern = r"Фамилия/Surname\n(.*?)\n"
            given_names_pattern = r"Имя/Given names\n(.*?)\n"
            nationality_pattern = r"Гражданство/Nationality\n(.*?)\n"
            place_of_birth_pattern = r"Место рождения/Place of birth\n(.*?)\n"
            gender_pattern = r"/Sex\n(.*?)\n"
            # mrz_pattern = r"([A-Z0-9<]+)<<([A-Z]+)<<([A-Z]+)<<([A-Z0-9<]+)<<"

            translator = Translator()

            try:
                surname_match = re.search(surname_pattern, passport_text)
                surname_ru = surname_match.group(1)
                surname_ru = surname_ru.strip('/').rstrip(' ')
                surname_en = translator.translate(surname_ru, src='ru', dest='en').text
            except:
                surname_en = ''

            try:
                given_names_match = re.search(given_names_pattern, passport_text)
                given_names_ru = given_names_match.group(1)
                given_names_ru = given_names_ru.strip('/').rstrip(' ')
                given_names_en = translator.translate(given_names_ru, src='ru', dest='en').text
                given_names_en = given_names_en
            except:
                given_names_en = ''

            try:
                passport_number_match = re.search(passport_number_pattern, passport_text)
                passport_number = passport_number_match.group(1)
                # passport_number_en = translator.translate(, src='ru', dest='en').text
            except:
                passport_number = ''

            try:
                nationality_match = re.search(nationality_pattern, passport_text)
                nationality_ru = nationality_match.group(1)
                nationality_ru = nationality_ru.split('/')[-1]
                nationality_en = translator.translate(nationality_ru, src='ru', dest='en').text
            except:
                nationality_en = 'RUSSIAN FEDERATION'

            try:
                place_of_birth_match = re.search(place_of_birth_pattern, passport_text)
                place_of_birth_ru = place_of_birth_match.group(1)
                place_of_birth_en = translator.translate(place_of_birth_ru, src='ru', dest='en').text
            except:
                place_of_birth_en = ''
            
            try:
                dates = re.findall(date_pattern, passport_text)
                date_objects = [datetime.strptime(date, '%d.%m.%Y') for date in dates]
                sorted_dates_asc = sorted(date_objects)
                sorted_dates_asc_str = [date.strftime('%d.%m.%Y') for date in sorted_dates_asc]

                date_of_birth, date_of_issue, date_of_expiry = sorted_dates_asc_str
            except:
                date_of_birth, date_of_issue, date_of_expiry = '', '', ''
            
            try:
                gender_match = re.search(gender_pattern, passport_text)
                gender = gender_match.group(1)
                gender = gender.split('/')[-1]
            except:
                gender = ''

            passport_details = {
                'passport_given_name_ru': given_names_ru,
                'passport_given_name_en': given_names_en,
                'passport_surname_ru': surname_ru,
                'passport_surname_en': surname_en,
                'paasport_number': passport_number,
                'passport_nationality': nationality_en,
                'passport_place_of_birth_ru': place_of_birth_ru,
                'passport_place_of_birth_en': place_of_birth_en,
                'passport_date_of_birth': date_of_birth,
                'passport_date_of_issue': date_of_issue,
                'passport_date_of_expiry': date_of_expiry,
                'passport_gender': gender
            }

            return passport_details


    def extract_ocr_info(self, data, video, country='UAE'):
        document_report = {}

        id_number = data.get('id_number')
        dob = data.get('dob')
        expiry_date = data.get('expiry_date')
        name = data.get('name')

        if not id_number:
            data['id_number'] = data.get('front_id_number')
        
        if not name:
            data['name'] = data.get('front_name')

        if not dob and data.get('front_dob'):
            data['dob'] = data.get('front_dob')
        
        if not expiry_date and data.get('front_expiry_date'):
            data['expiry_date'] = data.get('front_expiry_date')
        
        # print(f"\n\nFinal merged result: {data}")

        colour_picture = 'consider'
        if data.get('front_coloured') and data.get('back_coloured'):
            colour_picture = 'clear'

        blurred = 'clear'
        if data.get('front_blurred')=='consider' or data.get('back_blurred')=='consider':
            blurred = 'consider'
        
        glare = 'clear'
        if data.get('front_glare')=='consider' or data.get('back_glare')=='consider':
            glare = 'consider'

        missing_fields = 'clear'
        if data.get('front_missing_fields') or data.get('back_missing_fields'):
            missing_fields = 'consider'

        if video:
            selfie = self.extract_selfie_from_video(video)
            
            # front_face_locations = data.get('front_face_locations')
            # front_face_encodings = data.get('front_face_encodings')

            face_loc = json.loads(data.get('front_face_locations'))
            front_face_locations = tuple(face_loc)
            front_face_encodings = np.array(json.loads(data.get('front_face_encodings')))

            data['front_face_locations'] = front_face_locations
            data['front_face_encodings'] = front_face_encodings

            similarity = self.extract_face_and_compute_similarity(selfie, front_face_locations, front_face_encodings)
            
        else:
            selfie = None
            similarity = 0

        # front_face_locations, front_face_encodings = data.get('front_face_locations'), data.get('front_face_encodings')
        # processed_selfie = self.process_image(selfie)

        document_report = form_final_data_document_report(data, data.get('front_extracted_data'), data.get('back_extracted_data'), colour_picture, selfie, similarity, blurred, glare, missing_fields)
        
        if video:
            liveness_result = self.check_for_liveness(similarity, video)
        else:
            liveness_result = None

        facial_report = form_final_facial_similarity_report(selfie, similarity, liveness_result)

        # else:
        #     pass
        
        #json_object = json.dumps(df, indent = 4) 
        return document_report, facial_report
