# TriNetra  
*A Contactless Real-Time Heart Monitoring & Alert Generation System*
![Image](https://github.com/user-attachments/assets/beba8442-6222-40b6-b160-cbc6184035db)


## 🚀 Overview  




https://github.com/user-attachments/assets/4400a3f0-5a9f-4742-a62a-525357105498





TriNetra is an advanced real-time health monitoring system that leverages SpO2 detection, heart rate monitoring, and alert generation mechanisms to provide timely health insights. The system is designed to assist individuals in monitoring their vital signs and alert them in case of anomalies.
## 🚀Problem Statement
- **Non-Invasive:** Chest straps and heart rate machines require contact, causing discomfort and limiting continuous use. 

- **Medical Waste:** Disposable monitoring devices contribute 15-20% of the 2 million tons of healthcare waste annually. 

- **Cost-Ineffective:** Traditional heart rate monitors range from ₹4,000 to ₹24,000, making them less accessible for continuous, non-contact monitoring.

- **Late Response Time:** Many conventional devices have delays in detecting real-time heart rate changes, reducing effectiveness in critical situations.


 
## 📌 Features  
✔️ Real-time **heart rate detection**  
✔️ Accurate **SpO2 (Oxygen Saturation) measurement**  
✔️ Automated **alert generation** in case of abnormal readings  
✔️ Modular and **scalable architecture** for easy integration  
✔️ User-friendly and lightweight **Python-based implementation**  

## 🛠 Methodology
![Image](https://github.com/user-attachments/assets/3a1547b0-1d58-4737-be32-58cdce184c46)
- Capture facial video data to extract regions of interest (ROI) for analysis.  
- Isolate green and red color channels from the video frames, as they correlate with blood flow and oxygen saturation.  
- Transmit processed frames to a Jetson module for real-time edge computing.  
- Utilize MediaPipe for face tracking or landmark detection to ensure consistent ROI alignment.  
- Apply temporal smoothing filters to reduce noise in the color channel signals.  
- Convert the smoothed temporal signals to the frequency domain using Fast Fourier Transform (FFT).  
- Filter the frequency domain within the 0.7–4 Hz range to isolate heart rate and physiological signals.  
- Amplify subtle signal variations using Eulerian Video Magnification (EVM) for enhanced detection.  
- Analyze amplified signals to estimate heart rate (HR) by identifying dominant frequencies.  
- Compute SpO2 levels by analyzing ratios of light absorption in red and green channels.  
- Monitor for anomalies, such as abrupt spikes or drops in HR or SpO2 values.  
- Trigger alerts if anomalies are detected to notify users or healthcare providers.
## 🛠 Tech Stack  
- **Programming Language:** Python  
- **Libraries Used:** OpenCV, NumPy, SciPy, Matplotlib, PySerial, etc. *(Mention key dependencies used in your project.)*  

## 🏗 Future Enhancements
-  📌 Integration with IoT devices for remote monitoring
-  📌 Mobile app support for notifications and alerts
-  📌 AI-based anomaly detection for predicting potential health risks

## 📞 Contact & Support
- 📧 Email: shivammehtadcm@gmail.com
- 📧 Email: rishikesh7shukla@gmail.com
