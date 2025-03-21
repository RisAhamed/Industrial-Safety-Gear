# 🚀 Industry Safety Detection (YOLOv7)  

## 📌 Overview  
Industry Safety Detection is a computer vision-based project using **YOLOv7** to detect safety equipment violations in an industrial setting. The project follows an MLOps approach, implementing components like **Data Ingestion, Data Validation, Model Training, Model Pushing, Deployment, and CI/CD using AWS & Docker**.

---

## 📂 Project Structure  

```
📦 Industry-Safety-Detection
│── 📁 isd
│   ├── 📁 components
│   ├── 📁 configuration
│   ├── 📁 constants
│   ├── 📁 entity
│   ├── 📁 exception
│   ├── 📁 logger
│   ├── 📁 pipeline
│   ├── 📁 utils
│── 📁 notebooks
│── 📁 artifacts
│── 📁 templates
│── app.py
│── Dockerfile
│── requirements.txt
│── setup.py
│── README.md
│── .gitignore
│── .dockerignore
│── .github/workflows/cicd.yaml
```

---

## 🛠 Setup Instructions  

### 🔹 Step 1: Create a GitHub Repository & Clone It Locally  
```bash
git init
git remote add origin <YOUR_GITHUB_REPO_URL>
git pull origin main
```

---

### 🔹 Step 2: Setup Virtual Environment  
```bash
conda create -n yolo python=3.8 -y
conda activate yolo
```

---

### 🔹 Step 3: Install Dependencies  
```bash
pip install -r requirements.txt
```

---

### 🔹 Step 4: Initialize the Project  
Create a **template file** and run it to verify the setup:  
```bash
touch template.py
python template.py
```

---

### 🔹 Step 5: Setup Logging & Exception Handling  
Update the following files:  
- `object/logger/__init__.py`
- `object/exception/__init__.py`
- `object/utils/main_utils.py`

---



## 📥 Data Ingestion  
you can get the data set from either kaggle or Roboflow , 
the roboflow dataset used is publicly available.
```bash 
https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow
```
once downloaded upload the zip file to the s3 bucket and change the bucket name  and the file name in the constants constants[object\constant\__init__.py] file.


### 🔹 Step 7: Setup AWS CLI & Configure S3  
1. **Install AWS CLI**  
   - Google "AWS CLI download" → Choose OS → Download `.msi` → Install → Restart IDE.  

2. **Create an IAM User (name: yolov7) & Configure AWS Access**  
   - IAM Permissions:  
     - `AmazonEC2ContainerRegistryFullAccess`  
     - `AmazonEC2FullAccess`  
   - Configure AWS credentials:  
     ```bash
     aws configure
     ```
     - Input **Access Key, Secret Key, Region**.

3. **Create an S3 Bucket & Upload Data**  
   - Name: `industry-safety-data`  
   - Uncheck **Block Public Access**  
   - Upload **zipped dataset**  

4. **Update Configuration for S3 Data Retrieval**  
   - Implement logic in `object/configuration/s3_operations.py`.

---

## ✅ Data Validation  

Ensure that after extracting the zip file, the necessary directories and files exist inside **feature_store**.

---

## 🏗 Model Training  

### 🔹 Step 8: Download YOLOv7 Repo & Configure Custom Training  
```bash
git clone https://github.com/WongKinYiu/yolov7
```
- Copy `yolov7/data/coco.yaml` → Rename as **custom.yaml** → Modify it.  
- Copy `yolov7/cfg/training/yolov7.yaml` → Rename as **custom_yolov7.yaml** → Modify (`nc: 5`).  

### 🔹 Step 9: Train Model  
Run:  
```bash
python app.py
```
- The best model will be saved as:  
  ```text
  artifacts/<timestamp>/model_trainer/best.pt
  ```

---

## 🚀 Model Deployment  

### 🔹 Step 10: Update Web App for Prediction  
1. Modify `templates/index.html` (Update **title at line 200**).  
2. Ensure `app.py` is correctly configured (Model path: **yolov7/best.pt**).  
3. Run the Web App:  
   ```bash
   python app.py
   ```

---

## 🏗️ CI/CD Pipeline  

### 🔹 Step 11: Setup CI/CD in GitHub  
1. **Create `.github/workflows/cicd.yaml`**  
   - Ensure the pipeline does not include `sudo apt-get update` in **Continuous Delivery Stage** if it causes issues.

2. **Create a Dockerfile & .dockerignore**  
   ```dockerfile
   FROM python:3.8
   WORKDIR /app
   COPY . .
   RUN pip install -r requirements.txt
   CMD ["python", "app.py"]
   ```
   Add items like flowcharts, notebooks, `env`, logs to `.dockerignore`.

---

## 🔗 AWS Deployment  

### 🔹 Step 12: Setup AWS ECR & EC2  

1. **Create an AWS ECR Repository**  
   - Region: `us-east-1`  
   - Name: `yolov7app`  
   - Copy repository URI.  

2. **Launch an EC2 Instance**  
   - **OS**: Ubuntu 20.04  
   - **Instance Type**: `t2.large` (8GB RAM)  
   - **Key Pair**: `yolov7-key.pem`  
   - **Security Group**: Allow **all traffic**  
   - **Storage**: 32GB  
   - **Launch Instance**  

---

### 🔹 Step 13: Install Docker on EC2  
SSH into EC2 instance & run:  
```bash
# Optional
sudo apt-get update -y
sudo apt-get upgrade

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

---

### 🔹 Step 14: Setup Self-Hosted Runner on EC2  
1. **Go to GitHub Repo → Settings → Actions → Runners**  
2. **Follow Instructions to Setup a Runner (name: self-hosted)**  

---

### 🔹 Step 15: Configure GitHub Secrets  
Go to **GitHub Repo → Settings → Secrets and Variables → Actions**  
Add the following secrets:  
```text
AWS_ACCESS_KEY_ID 
AWS_SECRET_ACCESS_KEY 
AWS_REGION 
AWS_ECR_LOGIN_URI
ECR_REPOSITORY_NAME 
```

---

### 🔹 Step 16: Push Code & Run CI/CD  
```bash
git add .
git commit -m "Initial commit"
git push origin main
```
The pipeline should automatically build and deploy the model.

---

## 🔍 Check Deployment  
1. **Add Port 8080 to EC2 Security Group**  
2. **Check Deployment on Browser**:  
   ```text
   http://<EC2-PUBLIC-IP>:8080
   ```

---

## 🗑 Cleanup (Avoid AWS Charges)  
1. Delete **EC2 Instance**.  
2. Delete **ECR Repository**.  
3. Delete **S3 Bucket**.  

---

## 📌 Workflow  

✔ **Data Ingestion** →  
✔ **Data Validation** →  
✔ **Model Training** →  
✔ **Model Pushing** →  
✔ **CI/CD Pipeline** →  
✔ **Deployment on AWS**

---

## 🏆 Conclusion  
This project implements **YOLOv7 for industry safety detection**, following a structured **MLOps** approach with **AWS, Docker, and CI/CD**. 🚀  
😊
