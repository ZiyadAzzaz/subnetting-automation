cat << 'EOF' > README.md
# 🧮 Subnetting Automation in Python

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Network Tool](https://img.shields.io/badge/category-Networking-lightgrey)](https://en.wikipedia.org/wiki/Subnetwork)
[![Made by Ziyad Azzaz](https://img.shields.io/badge/author-ZiyadAzzaz-blueviolet)](https://github.com/ZiyadAzzaz)

A Python tool for automating IP subnet allocation based on host requirements. It calculates optimized subnets, displays key details (range, broadcast, mask, etc.), and visualizes the entire topology using **NetworkX** and **Matplotlib**.

---

## 📌 Features

- 🔢 Converts host requirements into optimal subnet prefixes
- 🧾 Computes:
  - Usable host range
  - Subnet mask
  - Broadcast address
  - Binary representations
- 📈 Generates a **topology graph** of subnets using `networkx`
- ❗ Handles invalid input and edge cases robustly
- 💡 Interactive CLI input for flexibility

---

## 🛠️ Usage

### ▶️ Run the tool
```bash
python3 subnetting.py
