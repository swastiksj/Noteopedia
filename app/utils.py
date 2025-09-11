import cloudinary.uploader
import cloudinary

def upload_pdf_to_cloudinary(file, filename):
    # Upload PDF as raw (not image)
    upload_result = cloudinary.uploader.upload(
        file,
        resource_type="raw",
        folder="noteopedia_pdfs"
    )

    # Get public_id and version
    public_id = upload_result["public_id"]
    version = upload_result["version"]

    # Generate download URL with forced download and original filename
    download_url = (
        f"https://res.cloudinary.com/{cloudinary.config().cloud_name}/raw/upload/"
        f"fl_attachment:{filename}/v{version}/{public_id}"
    )

    return download_url
