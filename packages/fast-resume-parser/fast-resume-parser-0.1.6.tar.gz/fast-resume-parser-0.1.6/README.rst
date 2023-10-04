Fast Resume Parser
=================

This is a Fast application for parsing resumes uploaded by users. The application supports PDF, DOC, and DOCX file formats. When a resume is uploaded, the application extracts text from the file, processes it, and generates a JSON response containing specific fields like name, email, phone number, total experience, profession, address, description, gender, date of birth, country, city, postcode, and state.

Github Url
----------
:doc:`fast-resume-parser on PyPI <https://github.com/devlobb/fastapi-resume-parser/>`

Installation
------------

1. **Install:**

   .. code-block:: bash

      pip install fast-resume-parser

2. **Import the ResumeParser class:**

   .. code-block:: python

      from fast_resume_parser.resume_parser import ResumeParser

3. **Initialize the ResumeParser class with your OpenAI API key:**

   .. code-block:: python

      # Provide the full file path of the resume file you want to parse
      file_path = "path/to/your/resume.pdf"

      # Use the parser to parse the resume file
      resume_data = await parser.parse_resume(file_path)

      # 'resume_data' now contains the parsed data from the resume file
      print(resume_data)

4. **Input:**

   file: The resume file (PDF, DOC, or DOCX) to be uploaded.

5. **Output:**

   * **200 OK:** Resume parsed successfully. JSON response containing parsed user data.

   .. code-block:: bash

      { 
          "message": "File parsed successfully", 
          "user": {
              "name": "John Doe",
              "email": "john.doe@example.com",
              "phone": "123-456-7890",
              "total_exp": "5 years",
              "profession": "Software Developer",
              "address": "123 Main St, Cityville, State, 12345",
              "description": "Experienced software developer with a passion for coding...",
              "gender": "Male",
              "dob": "1990-01-01",
              "country": "United States",
              "city": "Cityville",
              "postcode": "12345",
              "state": "State"  
          } 
      }

   * **400 Bad Request:** Unsupported file type. JSON response containing an error message.

   .. code-block:: bash

      {
          "error": "Unsupported file type"
      }

   * **500 Internal Server Error:** Error occurred while processing the file. JSON response containing an error message.

   .. code-block:: bash

      {
          "error": "Internal server error"
      }

Contributing
------------

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on GitHub. Pull requests are also appreciated.

License
-------

This project is licensed under the MIT License - see the LICENSE file for details.
