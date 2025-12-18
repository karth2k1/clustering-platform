# Expert View & Jupyter Notebook Setup

The **Expert View** mode generates interactive Jupyter notebooks that allow you to modify and experiment with the clustering code directly.

## Prerequisites

Jupyter must be installed to use Expert View notebooks.

### Installation

```bash
cd backend
python3 -m pip install --break-system-packages jupyter jupyterlab notebook
```

Or add to your `requirements.txt` and install:
```bash
pip install -r requirements.txt
```

## Starting the Jupyter Server

The Expert View generates notebooks in `backend/notebooks/` directory. To view and run them:

### Option 1: Manual Start (Recommended for Development)

```bash
cd backend
jupyter notebook --notebook-dir=./notebooks --port=8888 --no-browser
```

This will:
- Start Jupyter on http://localhost:8888
- Serve notebooks from `backend/notebooks/`
- Display a URL in the terminal with an access token

### Option 2: Background Start (No Authentication)

```bash
cd backend
jupyter notebook --notebook-dir=./notebooks --port=8888 --no-browser \
  --NotebookApp.token='' --NotebookApp.password='' &
```

**⚠️ Warning:** This disables authentication. Only use on trusted local networks!

### Option 3: Using JupyterLab (Modern Interface)

```bash
cd backend
jupyter lab --notebook-dir=./notebooks --port=8888 --no-browser
```

## Using Expert View

1. **Start Backend**: `python run.py` (from `backend/` directory)
2. **Start Frontend**: `npm run dev` (from `frontend/` directory)
3. **Start Jupyter**: Use one of the options above
4. **Upload Data**: In the web UI, upload your dataset
5. **Select Expert View**: Choose "Expert View (Jupyter Notebook)"
6. **Configure & Run**: Fill in the questionnaire and click "Generate Notebook"
7. **Open Notebook**: Click the provided link (e.g., `http://localhost:8888/notebooks/clustering_xxx.ipynb`)

## What You Get in the Notebook

The generated notebook includes:

- **Data Loading**: Pre-configured code to load your dataset
- **Preprocessing**: Data cleaning and transformation steps
- **Clustering**: Multiple algorithms (K-Means, DBSCAN, HDBSCAN)
- **Visualization**: Interactive plots and charts
- **Evaluation**: Metrics and cluster quality assessment
- **Editable Cells**: Modify any part of the code and re-run

## Tips for Expert View

### Modifying the Notebook

- ✅ **Change Parameters**: Adjust `n_clusters`, `eps`, `min_samples`, etc.
- ✅ **Add Algorithms**: Import and test new clustering methods
- ✅ **Custom Visualizations**: Use matplotlib, seaborn, plotly
- ✅ **Feature Engineering**: Add new features or transformations
- ✅ **Export Results**: Save clustered data to CSV

### Common Modifications

**Change number of clusters:**
```python
# Find the K-Means section and change:
kmeans = KMeans(n_clusters=5)  # Change from 3 to 5
```

**Add different visualization:**
```python
import seaborn as sns
sns.pairplot(df_clustered, hue='cluster', palette='Set2')
plt.show()
```

**Try different preprocessing:**
```python
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()  # Instead of StandardScaler
```

## Troubleshooting

### "Jupyter not found"

Install Jupyter:
```bash
python3 -m pip install --break-system-packages jupyter
```

### "Cannot connect to http://localhost:8888"

Make sure Jupyter server is running:
```bash
# Check if running
lsof -i :8888

# If not, start it
jupyter notebook --notebook-dir=./backend/notebooks --port=8888
```

### "Kernel not found" or "No module named 'pandas'"

The notebook needs access to the same packages as the backend. Install in your Python environment:
```bash
pip install --break-system-packages pandas numpy scikit-learn matplotlib seaborn plotly hdbscan
```

Or:
```bash
cd backend
pip install --break-system-packages -r requirements.txt
```

### Port 8888 Already in Use

Either:
1. Find and stop the existing Jupyter server:
   ```bash
   lsof -i :8888
   kill <PID>
   ```

2. Use a different port:
   ```bash
   jupyter notebook --port=8889
   ```
   Then update the URL to use port 8889.

### Notebook Shows "Untrusted"

Click the "Trust" button in the top-right corner of the notebook interface.

## Security Notes

- 🔒 **Local Development**: Authentication is disabled for convenience
- 🌐 **Production**: Never expose Jupyter to public networks without authentication
- 🔑 **Tokens**: Use `--NotebookApp.token='your-secret-token'` for remote access
- 🔐 **Passwords**: Set up a password with `jupyter notebook password`

## Advanced Configuration

### Create Jupyter Config File

```bash
jupyter notebook --generate-config
```

Edit `~/.jupyter/jupyter_notebook_config.py`:
```python
c.NotebookApp.notebook_dir = '/path/to/clustering-platform/backend/notebooks'
c.NotebookApp.port = 8888
c.NotebookApp.open_browser = False
```

### Run as a Service (macOS/Linux)

Create a launch daemon or systemd service to start Jupyter automatically on boot.

## Resources

- [Jupyter Documentation](https://jupyter.org/documentation)
- [JupyterLab Documentation](https://jupyterlab.readthedocs.io/)
- [Scikit-learn Clustering](https://scikit-learn.org/stable/modules/clustering.html)

## Summary

```bash
# Quick Start (3 commands)
1. cd backend && python3 -m pip install --break-system-packages jupyter
2. jupyter notebook --notebook-dir=./notebooks --port=8888 &
3. # Use Expert View in the web UI - notebooks will open automatically!
```

---

**Now you're ready to use Expert View! 🚀**

