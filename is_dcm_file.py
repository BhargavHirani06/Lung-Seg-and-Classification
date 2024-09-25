import os

def check_dcm(file_path):
    """Checks if the given file path points to a DICOM file."""

    # Simple check for the .dcm extension
    if not file_path.lower().endswith(".dcm"):
        return False

    # Additional check using pydicom (if available)
    try:
        import pydicom
        pydicom.dcmread(file_path, stop_before_pixels=True)  # Read header only
        return True
    except (ImportError, pydicom.errors.InvalidDicomError):
        return False  # Not a valid DICOM file
