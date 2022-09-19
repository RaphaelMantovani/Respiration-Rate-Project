# Respiration-Rate-Project

This project is using computer vision to calculate the respiration rate of lying dairy cows. By analyzing the difference in average pixel intensity in annotated bounding boxes and performing Fast Fourier Transform to select the most prevalent data, this model predicts the number of times a cow breathed in a 30-second interval. The frame_capture.py file was used to save a frame from each saved test video, while the respiration_rate_automated.py is the model used to predict each cow's respiration rate. All directories are based on my computer. An example of video frame, average pixel intensity, and cleaned and predicted data is as follows:

![CAM11_video1_Trim_Moment](https://user-images.githubusercontent.com/91127693/191072946-2e7712f0-10ec-4342-89bb-7d3f4316e114.jpg)
![pixel_intensity_test_data](https://user-images.githubusercontent.com/91127693/191072822-9bde50cd-b497-4b85-84a7-7c686b1babf3.png)
![find_peaks_test2](https://user-images.githubusercontent.com/91127693/191072821-a3098580-0f25-4328-a63c-6986000b280d.png)
