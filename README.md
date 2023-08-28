## Certificate Management System Readme

This repository contains code for a Certificate Management System implemented using Flask and Polygon blockchain based on Etereum. The system allows users to create, view, and verify certificates securely on the blockchain.

### Prerequisites

1. **Python**: Make sure you have Python 3.x installed on your system.

2. **MongoDB**: You need a MongoDB database to store user and certificate information. Update the MongoDB connection URI in both `Server.py` and `Generator.py` to point to your MongoDB instance.

3. **Web3.py**: Ethereum blockchain interaction is done using the `web3.py` library. You can install it using `pip install web3`.

4. **Flask and Dependencies**: Install Flask and other required dependencies using `pip install Flask Flask-Session pymongo flask_apscheduler solcx`.

### How to Run

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/Om-Mishra7/KRMU-OS-Expo_2023.git
   cd KRMU-OS-Expo_2023
   ```

2. Install the required dependencies as mentioned in the **Prerequisites** section, by running the following command:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask server by running the `Server.py` script:

   ```bash
   python Server.py
   ```
   or 
   ```bash
    python3 Server.py
    ```

   This will start the Flask application on `http://127.0.0.1:5000/`.

4. Access the application in your web browser by navigating to `http://127.0.0.1:5000/`.

### Features

- **Sign Up / Sign In**: Users can sign up using their email and password or sign in if they already have an account.

- **Dashboard**: After logging in, users can access their dashboard to view the status of their certificates.

- **Create Certificate**: Users can create certificates by providing necessary details such as student name, CGP, certificate title, issuing authority, and issuing date.

- **Verify Domain**: Users need to verify their email domain before using the system. Verification is done using DNS TXT records.

- **View Certificate**: Users can view their certificates and see the details associated with them.

- **Blockchain Integration**: The application integrates with the Ethereum blockchain to securely store certificate data.

- **Certificate Generation**: The `Generator.py` script generates certificates on the blockchain. It compiles a Solidity smart contract, deploys it to the blockchain, and interacts with it to store certificate details.

- **Certificate Processing**: The `process_data` function in `Generator.py` processes pending certificates and generates their corresponding blockchain entries.

### Additional Notes

- The application uses the Flask framework for the web interface and MongoDB for database storage.

- Blockchain integration is achieved using the Polygon blockchain and the `web3.py` library.

- The certificate generation process involves compiling and deploying a Solidity smart contract to the blockchain.


The Certificate Management System presented in your provided code implements a unique and innovative approach to certificate issuance, storage, and verification. Here are some reasons why this idea can be considered unique:

1. **Blockchain Integration for Certificates**: The system leverages the Ethereum blockchain to store certificate data securely. Blockchain technology ensures immutability and transparency, making it an ideal solution for storing sensitive information like certificates. This ensures that once a certificate is generated and stored on the blockchain, it cannot be altered or tampered with, providing a high level of trust and authenticity.

2. **Decentralized Verification**: The system uses DNS TXT records to verify email domain ownership. This approach decentralizes the verification process, as it utilizes the inherent structure of the DNS system. This is a creative way to validate users' ownership of their email domains and adds an additional layer of security.

3. **Automated Certificate Generation**: The integration of an automated certificate generation process using Solidity smart contracts is a novel feature. This process streamlines the certificate creation and storage process by executing it directly on the blockchain. This can significantly reduce the need for manual intervention and potential errors.

4. **User-Friendly Interface**: The Flask-based web interface simplifies the user experience, making it easy for users to create, view, and manage their certificates. The system's dashboard provides a clear overview of certificate statuses, enhancing user transparency and control.

5. **Combination of Technologies**: The integration of Flask, MongoDB, and Ethereum blockchain in a single application is a unique combination of technologies. This combination enables seamless user interaction, efficient data storage, and secure certificate management.

6. **Potential for Extensibility**: The concept of using a blockchain-backed certificate management system has broad applicability. It can be extended for various use cases, including educational institutions issuing digital degrees, organizations providing digital badges, and more.

7. **Integration of Blockchain into Existing Processes**: The system doesn't just add blockchain for the sake of it; it integrates blockchain into a practical use case. This integration showcases how blockchain technology can enhance existing processes, such as certificate issuance and verification.

8. **Real-World Use Case**: The system addresses a real-world problem: verifying the authenticity of certificates. The use of blockchain and decentralized domain verification contributes to a more secure and reliable certificate ecosystem, which can be particularly beneficial in contexts where digital certificates are used.

In conclusion, the Certificate Management System you've described combines various technologies in a unique way to address the challenges of certificate issuance, storage, and verification. Its use of blockchain, decentralized verification, and automated generation sets it apart as an innovative solution in the field of digital credentials and certificate management.


Thank you for hosting the KRMU-OS-Expo_2023 Hackathon! The Certificate Management System presented here is a testament to the innovative ideas and creative thinking that emerge from such events. The combination of blockchain technology, decentralized verification, and automated certificate generation showcases the potential for transforming traditional processes into more secure and efficient solutions.

I hope you find this project useful and look forward to hearing your feedback. Please feel free to reach out if you have any questions or suggestions.

Best regards,
Team Innova8ors

[Om Mishra](https://github.com/Om-Mishra7)
[Yash Soni](https://github.com/Yash-Soni7744)


