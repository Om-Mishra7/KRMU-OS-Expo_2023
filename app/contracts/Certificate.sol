// SPDX-License-Identifier: MIT
pragma solidity >=0.8.0;

contract Certificate {

    struct CertificateBody {
        string CertificateID;
        string StudentName;
        string StudentCGP;
        string StudentProfilePictureUrl;
        string CertificateTitle;
        string IssuingAuthority;
        string IssuingDate;
    }

    CertificateBody internal certificate;

    address public certSecureAddress;

    constructor() {
        certSecureAddress = msg.sender;
    }

    event AccessDenied(address indexed currentAddress, address indexed certSecureAddress);

    modifier verifyCertSecureAddress {
        if (msg.sender != certSecureAddress) {
            emit AccessDenied(msg.sender, certSecureAddress);
            revert("Access denied.");
        }
        _;
    }

    function generateCertificateBody(
        string memory _CertificateID,
        string memory _StudentName,
        string memory _StudentCGP,
        string memory _StudentProfilePictureUrl,
        string memory _CertificateTitle,
        string memory _IssuingAuthority,
        string memory _IssuingDate
    ) public verifyCertSecureAddress {
        certificate = CertificateBody({
            CertificateID: _CertificateID,
            StudentName: _StudentName,
            StudentCGP: _StudentCGP,
            StudentProfilePictureUrl: _StudentProfilePictureUrl,
            CertificateTitle: _CertificateTitle,
            IssuingAuthority: _IssuingAuthority,
            IssuingDate: _IssuingDate
        });
    }

    function getCertificateBody() public view returns (
        string memory,
        string memory,
        string memory,
        string memory,
        string memory,
        string memory,
        string memory
    ) {
        // Return dummy data since this is a pure function
        return (certificate.CertificateID, certificate.StudentName, certificate.StudentCGP, certificate.StudentProfilePictureUrl, certificate.CertificateTitle, certificate.IssuingAuthority, certificate.IssuingDate);
    }
}
