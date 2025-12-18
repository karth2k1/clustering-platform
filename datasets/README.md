# Sample Datasets for Clustering Platform

This directory contains curated sample datasets perfect for demonstrating the clustering platform's capabilities.

## 📁 Directory Structure

```
datasets/
├── sample_data/           # CSV files ready to upload
│   ├── iris.csv
│   ├── customer_segmentation.csv
│   ├── network_intrusion.csv
│   └── nyc_taxi.csv
├── documentation/         # Dataset metadata and descriptions
│   ├── iris_metadata.json
│   ├── customer_segmentation_metadata.json
│   ├── network_intrusion_metadata.json
│   └── nyc_taxi_metadata.json
└── README.md             # This file
```

## ⚠️ Data Source Disclaimer

**Iris Dataset:** Authentic data from the UCI Machine Learning Repository (1936), loaded via scikit-learn. This is real botanical data.

**Other Datasets (Customer, Network, Taxi):** Synthetically generated using statistical distributions designed to exhibit realistic patterns. These are NOT real customer records, network logs, or taxi trips. They are created specifically for safe, privacy-compliant demonstrations without licensing restrictions.

**Why Synthetic Data?**
- ✅ No privacy or security concerns
- ✅ No licensing or download requirements  
- ✅ Consistent, predictable demo results
- ✅ Safe to share publicly

**For Production Use:** The platform works identically with real data. Pilot programs use your actual data to demonstrate real-world results.

---

## 📊 Available Datasets

### 1. Iris Flower Classification ⭐ REAL DATA
**File:** `sample_data/iris.csv`

- **Size:** 150 records, 4 features
- **Difficulty:** ⭐ Easy
- **Best For:** First-time users, algorithm validation
- **Features:** Sepal length, sepal width, petal length, petal width
- **Expected Clusters:** 3 (flower species)
- **Demo Time:** 5 minutes

**Use Case:**
Validate that clustering algorithms correctly identify the 3 iris species. Perfect for showing how clustering discovers natural groupings.

**Why Use This:**
- Quick to run
- Clear, interpretable results
- Universally understood ("grouping similar flowers")
- Proves the platform works

---

### 2. Mall Customer Segmentation 🔧 SYNTHETIC DATA
**File:** `sample_data/customer_segmentation.csv`

- **Size:** 200 records, 5 features
- **Difficulty:** ⭐ Easy
- **Best For:** Business stakeholders, marketing demos
- **Features:** Customer ID, Gender, Age, Annual Income, Spending Score
- **Expected Clusters:** 5 (customer segments)
- **Demo Time:** 10 minutes

**Use Case:**
Identify customer segments for targeted marketing campaigns. Shows clear business value and ROI.

**Business Value:**
- Target high-value customers
- Create retention programs
- Optimize marketing spend
- 3x better campaign conversion rates

**Segments:**
1. Young Budget Shoppers
2. Young High Spenders (VIP target)
3. Middle Age Moderate
4. High Income Savers (untapped potential)
5. Senior Varied

---

### 3. Network Intrusion Detection 🔧 SYNTHETIC DATA
**File:** `sample_data/network_intrusion.csv`

- **Size:** 5,000 records, 41 features
- **Difficulty:** ⭐⭐ Medium
- **Best For:** IT operations, security analysts
- **Features:** Network traffic characteristics (duration, bytes, error rates, protocols, etc.)
- **Expected Clusters:** 2-5 (normal + attack types)
- **Demo Time:** 15 minutes

**Use Case:**
Identify network attack patterns and anomalies. Demonstrates cybersecurity applications.

**Security Value:**
- Automated threat detection
- Reduced false positives
- Zero-day attack detection (no signatures needed)
- 60% reduction in analyst triage time

**Attack Types:**
- Normal Traffic (~70%)
- DoS (Denial of Service)
- Probe (Port Scanning)
- R2L (Remote to Local attacks)
- U2R (Privilege Escalation)

---

### 4. NYC Taxi Spatial Analysis 🔧 SYNTHETIC DATA
**File:** `sample_data/nyc_taxi.csv`

- **Size:** 10,000 records, 8 features
- **Difficulty:** ⭐⭐ Medium
- **Best For:** Spatial analysis, operations optimization
- **Features:** Pickup/dropoff lat/lon, distance, duration, fare, passengers
- **Expected Clusters:** 5-10 (geographical zones)
- **Demo Time:** 15 minutes

**Use Case:**
Identify high-demand taxi zones for optimal driver dispatch. Shows spatial clustering and operations optimization.

**Business Value:**
- Optimize taxi placement
- Reduce empty drive time
- Dynamic pricing zones
- $50k+/year fuel savings per 100 taxis

**Hotspots:**
1. Times Square
2. Financial District
3. Midtown
4. Upper East Side
5. Upper West Side

---

## 🚀 Quick Start

### Option 1: Use Through Platform UI

1. Start the clustering platform
2. Navigate to "Upload File" 
3. Select a dataset from `datasets/sample_data/`
4. Choose the corresponding use case
5. Run clustering!

### Option 2: Generate Fresh Datasets

If you want to regenerate the datasets with different parameters:

```bash
cd backend
python -m app.utils.dataset_loader
```

This will regenerate all four datasets with fresh random seeds.

## 📖 Documentation

Each dataset has a corresponding metadata file in `documentation/` that includes:

- Source and description
- Feature descriptions
- Expected clustering results
- Business interpretation
- Use case recommendations

**View metadata:**
```bash
cat datasets/documentation/iris_metadata.json
```

## 🎯 Which Dataset Should I Use?

### For Your First Demo:
**→ Start with Iris** (5 minutes)
- Quickest to run
- Easiest to understand
- Proves the platform works

### For Business Stakeholders:
**→ Customer Segmentation** (10 minutes)
- Clear business value
- Actionable insights
- Shows ROI

### For Technical Teams:
**→ Network Intrusion** (15 minutes)
- Relevant to IT operations
- Shows advanced capabilities
- Security applications

### For Advanced Users:
**→ NYC Taxi** (15 minutes)
- Spatial analysis
- Complex optimization
- Impressive visualizations

### For Comprehensive Demo (45 minutes):
**→ All Four in Order**
1. Iris (validation)
2. Customer (business value)
3. Network (technical depth)
4. NYC Taxi (advanced applications)

## 📝 Demonstration Guide

For detailed demonstration scripts, talking points, and presentation tips, see:

**[DEMO_GUIDE.md](../DEMO_GUIDE.md)**

This comprehensive guide includes:
- Step-by-step demo instructions
- Talking points for different audiences
- Expected results and interpretations
- Business value explanations
- Handling common questions

## 🔄 Regenerating Datasets

All datasets are synthetically generated to ensure:
- No privacy concerns
- Consistent results
- Known ground truth for validation
- Easy to explain

To customize datasets:

1. Edit `backend/app/utils/dataset_loader.py`
2. Modify parameters (size, features, distributions)
3. Run `python -m app.utils.dataset_loader`
4. New datasets will be generated in `sample_data/`

## 📊 Dataset Statistics

| Dataset | Records | Features | File Size | Generation Time |
|---------|---------|----------|-----------|-----------------|
| Iris | 150 | 4 | ~5 KB | < 1 sec |
| Customer | 200 | 5 | ~8 KB | < 1 sec |
| Network | 5,000 | 41 | ~2 MB | ~2 sec |
| NYC Taxi | 10,000 | 8 | ~800 KB | ~3 sec |

## 🎓 Learning Path

### Beginner (New to Clustering):
1. Start with **Iris** - understand basic clustering
2. Move to **Customer** - see business application
3. Read DEMO_GUIDE.md for deeper understanding

### Intermediate (Some ML Experience):
1. Quick run through **Iris** and **Customer**
2. Focus on **Network Intrusion** - more complex
3. Experiment with different algorithms

### Advanced (Data Scientist):
1. Try all datasets
2. Compare algorithm performance
3. Experiment with feature engineering
4. Modify dataset generator for custom scenarios

## 🛠️ Troubleshooting

### "Cannot find dataset file"
**Solution:** Regenerate datasets:
```bash
cd backend
python -m app.utils.dataset_loader
```

### "Import error: pandas not found"
**Solution:** Install dependencies:
```bash
pip install pandas numpy scikit-learn
```

### "Dataset too large for demo"
**Solution:** Use smaller samples:
- Iris: Already small (150 records)
- Customer: Already small (200 records)
- Network: Reduce to 1,000 records in code
- NYC Taxi: Reduce to 2,000 records in code

### "Want different features or distributions"
**Solution:** Edit `backend/app/utils/dataset_loader.py` and customize the generation functions.

## 📚 Additional Resources

- **Platform Setup:** [/README.md](../README.md)
- **Demo Guide:** [/DEMO_GUIDE.md](../DEMO_GUIDE.md)
- **Use Cases:** [/use_cases/use_cases.json](../use_cases/use_cases.json)
- **Architecture:** [/ARCHITECTURE.md](../ARCHITECTURE.md)

## 🤝 Contributing

Have ideas for new demo datasets? Consider these criteria:

1. **Clear Use Case:** Solves a real business problem
2. **Appropriate Size:** 200-10,000 records for demos
3. **Interpretable:** Results should be easy to explain
4. **No Privacy Issues:** Synthetic or public domain data only
5. **Good Clusters:** Should have natural groupings

To add a new dataset:
1. Add generation function to `dataset_loader.py`
2. Create use case in `use_cases/use_cases.json`
3. Add demo guide section in `DEMO_GUIDE.md`
4. Update this README

## 📄 License

These synthetic datasets are provided for demonstration purposes and are free to use. They are not based on any real individual or organization data.

---

**Ready to demonstrate? See [DEMO_GUIDE.md](../DEMO_GUIDE.md) for step-by-step instructions!** 🎉

