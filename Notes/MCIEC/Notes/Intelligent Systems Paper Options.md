Paper Possible Subjects:
- quadruped robots artificial skin to improve terrain sensing capabilities
	- What options exist already?
- improvement options on simulation training for quadruped robots control system
- Ultrasonic sensing equipment as alternative to visual identification for terrain mobility:
- https://www.mdpi.com/2079-9292/13/24/4858

Paper Sections
- Abstract
- Index Terms
- Introduction
- Related works

Key concepts:
- [Neural Networks]
- Deep Learning
- Quantization
- neural architecture search, compression and pruning

### Deep Learning
A Comprehensive Review of Deep Learning: Architectures, Recent Advances, and Applications:
https://www.mdpi.com/2078-2489/15/12/755

### Neural Networks Papers
Neural Networks Fundamentals book:
https://aliosmangokcan.com/images/notes/yapay_sinir_agi_derin_ogrenme_pdf_ders_notu_e-book.pdf

A White Paper on Neural Network Quantization:
https://arxiv.org/pdf/2106.08295

A Systematic Literature Review on Binary Neural Networks:
https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=10072399

#### Machine Learning Papers

#### Computer Vision Papers
A review of convolutional neural networks in computer vision:
https://link.springer.com/article/10.1007/s10462-024-10721-6#additional-information

#### Pattern Recognition Papers

#### Quadruped Robot Papers

A Review of Quadruped Robots: Structure, Control, and Autonomous Motion:
https://advanced.onlinelibrary.wiley.com/doi/full/10.1002/aisy.202300783

### Options

### Option 3: The "Edge-Computing" Paper

**Refined Topic:** _Latency-Aware Policy Distillation: Performance Trade-offs in Quantized Neural Networks for Quadruped Locomotion_

- **The Shift:** Instead of "making a blind walking robot," you are investigating the _cost of compression_.
    
- **The "Scientific" Question:** "How much can we shrink (quantize) a walking Neural Network (from 32-bit float to 8-bit integer) before the robot loses its balance?"
    
- **Why this fits a Paper:**
    
    - **Method:** Train a standard "Teacher" policy that walks perfectly.
        
    - **Experiment:** "Distill" this policy into smaller "Student" networks (Float16, Int8).
        
    - **Result:** A curve plotting **Model Size (KB)** vs. **Walking Stability (Time to Fall)**.
        
    - **Publishable Conclusion:** "Our results indicate that 8-bit quantization retains 98% of walking performance while reducing inference time by 3x, enabling deployment on microcontrollers."


### Relation to classes and engineering fields
### Machine learning

##### Quadruped Robot
Papers:
- [Safe and Robust Motion Planning for Autonomous Navigation of Quadruped Robots in Cluttered Environments]

Key concepts:
- Aliengo Robot
- B-splines
- Motion characteristics of quadruped robots
- Navigation of quadruped robots, including navigation in unstructured terrains or unknown environments
- Navigation with multi-gait combinations
- The motion planning and autonomous navigation of robotic systems, the prevalent approach is to utilize a two-stage hierarchical architecture, which can be decomposed into front-end searching and back- end optimization
- kinodynamic searching
- Hybrid-state A
- motion primitives