# **Comparing Energy Consumption of H.264 and H.265 for Encoding and Decoding**

## **1. Introduction**
Software energy consumption has become a critical consideration in sustainable computing. As digital media consumption increases, video processing—specifically encoding and decoding—plays a significant role in global energy usage.

Video streaming platforms like YouTube serve billions of hours of video content, requiring significant energy for decoding on end-user devices. Understanding the energy footprint of different compression standards can help optimize power efficiency.

This blog explores the energy consumption of two widely used video codecs: H.264 and H.265 <!-- (Maybe also could ebe interesting to explore more codecs for decoding?? Like Apple ProRes).  --> We will analyze their energy efficiency in encoding <!-- well, we can do what youtube does, if it is not H.264 it converts the video to it, so it can be a compressed videos of different codec i guess--> and decoding, highlighting the implications of video streaming on energy consumption. <!--idk can be written better, redoo-->

---

## **2. Background & Motivation**
### **How Video Compression Works** <!--this is chatGpt generated so idk-->
Video compression reduces file size by removing redundant data, making streaming and storage more efficient. Compression algorithms achieve this by:
- Removing spatial and temporal redundancies.
- Using motion compensation and inter-frame compression.
- Applying entropy coding to store data more efficiently.

### **Common Video Formats: MP4, MOV, and Why H.264 is Dominant**
MP4 and MOV are common video formats used across devices. Most videos uploaded to YouTube are already compressed in MP4 (H.264) format. This makes H.264 the industry standard for video compression.

### **Introduction to H.265 and its Advantages Over H.264**
H.265 (HEVC) is a more advanced codec than H.264, offering:
- **Higher Compression Efficiency:** Up to 50% better compression <!--better compression meaning the size?! or anything else?? how much quality changes? if not significant then H.265c supposedly should be less energy consuming during video transmission--> than H.264 while maintaining quality.
- **Better Streaming Performance:** Requires less bandwidth for the same quality.
- **Increased Computational Complexity:** Higher decoding power consumption due to more complex algorithms.

### **Why Decoding Energy Consumption Matters** <!--Also ChatGpt generated but i like this heading, maybe can be moved above, motivation behind our work-->
With billions of hours of videos streamed daily, the energy required for decoding is significant. Efficient codecs can reduce the power consumption of devices and lower overall energy demand.

---

## **3. Experiment Setup**
### **Hardware & Software**
We will conduct tests on:
<!--computer, fixed environment settings, CPU, RAM and etc-->

### **Tools & Methods**
To measure energy consumption, we will use:

### **Metrics** <!--Data Collection-->
We will measure:
- **Encoding Power Consumption:** 
- **Decoding Power Consumption:** 

<!--probably can be a table in which is good to include file size initial before encoding/decoding and after
- **File Size Comparison:** Compression efficiency
 -->

### **Network Considerations** <!-- I have been reading few, we need to find ones that talk about per packet consumption, but im not sure, there are usually several hops involved when package is transmitted...-->
- **Larger file sizes lead to more data transmission.**
- **More transmitted data means increased energy consumption.**
- **Efficient compression can reduce streaming-related power consumption.**

---

## **4. Encoding Experiment**
### **Methodology**
1. Encode raw video files to H.264 and H.265.
2. Record power consumption during the encoding process.
3. Compare file sizes of the encoded outputs.
<!-- 4. Repeat experiment 30 times? Cooldown time and etc... i cant remember if we are asked to write about these -->

### **Metrics Collected**
- **Energy Consumption:** 
<!--Graphs could be nice-->
- **Encoding Time:** How long each codec takes to complete encoding.
- **File Size:** Impact of compression efficiency.

### **Results**
<!-- We will compare the energy usage of encoding in both codecs. -->

### **Discussion**
<!-- - Which codec is more energy-efficient for encoding?
- Does H.265’s higher compression efficiency offset its increased encoding complexity? -->

---

## **5. Decoding Experiment**
### **Methodology**

### **Metrics Collected**
- **Energy Consumption:** 
- **Decoding Time:** Time taken to decode each format.

### **Results**
<!-- A comparison of energy consumption when decoding both formats. -->

### **Discussion**
<!-- - Does H.265’s complexity increase playback power consumption?
- What are the implications for streaming platforms like YouTube? -->

---

## **6. Network Transmission Energy**
### **Impact of File Size**
- **Larger files require more data transfer.**
- **More data transfer increases network energy consumption.** <!--there are papers about it, reference again-->

### **Energy Cost of Streaming** <!--this is GPT generated fixxx-->
<!-- - Streaming higher-resolution videos requires significant bandwidth.
- Compression efficiency impacts streaming energy demand. -->

### **Comparison Between Codecs**
<!--I am supposing the following but we can check the results and see if true:-->
<!-- - H.265 reduces file size, lowering network energy consumption.
- However, increased decoding power requirements may offset savings. -->

---

## **7. Summary & Key Takeaways**
### **Recap of Findings**


### **Trade-offs Between Compression Efficiency and Decoding Energy**
<!-- - Efficient compression saves storage and bandwidth.
- Higher computational complexity may increase device power consumption. -->

### **Impact on Global Energy Consumption**
- Streaming billions of hours of video significantly contributes to energy usage.
- Optimizing codecs can reduce power demand in video streaming.

### **Potential Improvements**
<!-- if decoding H.265 is similar to H.264 and the file size is smaller and this the network transmission will consume less energy then H.265 should become a new standard. (Devices also should support this compression method) -->

---

## **8. Replication Package**
### **How to Reproduce the Experiment**


### **Resources Provided**
