# 🔧 NetConfig Enforcer

A lightweight command-line tool to automate static or dynamic IP configuration on Windows systems.

---

## 💡 Why I Built This

In the company I work at, I configured our Wi-Fi network in such a way that connecting with just the password won't grant internet access. Instead, the client must manually set a specific IP and gateway to access the network.

This script automates that process to avoid manual setup hassles for users.

---

## ⚙️ Features

- ✅ Detects active network interfaces (e.g., Ethernet or Wi-Fi)
- ✅ Sets static IP, subnet mask, gateway, and DNS servers
- ✅ Option to revert to DHCP with a single command
- ✅ Windows UAC elevation support (asks for Admin privileges)
- ✅ Simple terminal-based interactive menu
- ✅ Randomizes the last octet of the IP to avoid conflicts

---

## 🖥️ Screenshot

```
┌───────────────────────────────────┐
│      NETWORK CONFIG MANAGER       │
├───────────────────────────────────┤
│ Current Interface: Ethernet       │
├───────────────────────────────────┤
│ 1. Set Static IP                 │
│ 2. Enable DHCP                   │
│ 0. Exit                          │
└───────────────────────────────────┘
```

---

## 🚀 Getting Started

### 🔧 Requirements
- Windows OS
- Python 3.x
- Admin privileges (UAC prompt will be triggered automatically)

### ▶️ Usage

```bash
python netconfig.py
```

- When prompted, choose:
  - `1` to apply static IP settings (predefined IP range and DNS)
  - `2` to enable DHCP (automatic IP settings)
  - `0` to exit the app

---

## 🔐 Admin Elevation

This script automatically attempts to elevate itself with UAC on Windows if not already running as administrator.

---

## 🧠 How It Works

1. Detects the primary active network interface.
2. If the user selects static configuration:
   - Assigns a static IP: `192.168.1.X` where `X` is randomized between 100–195
   - Sets the gateway to: `192.168.1.254`
   - Sets DNS to: `8.8.8.8` and `4.2.2.4`
3. If DHCP is selected, reverts all changes back to automatic settings.

---

## 📁 Project Structure

```
netconfig/
├── netconfig.py      # Main script file
├── README.md         # This file
└── (Optional) .gitignore
```

---

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 🙌 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you'd like to change.

---

## 👨‍💻 Author

Built with 🔧 by [YourNameHere].  
Special thanks to all sysadmins who live in the terminal.

