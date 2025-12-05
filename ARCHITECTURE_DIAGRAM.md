# Architecture Diagram (Text Description)

```text
+-----------------------+         +-------------------------+        +----------------------------+
|  Browser (React UI)   |  HTTP   |   FastAPI Backend       |        |   AI / Image Processing   |
|-----------------------| <-----> |-------------------------| -----> |----------------------------|
| - File input (photo)  |         | /api/personalize        |        | - Face detection (stub)   |
| - "Generate" button   |         |                         |        | - Stylise + compose       |
| - Shows result image  |         | - Validates image file  |        |   onto story template     |
+-----------------------+         | - Loads template image  |        +----------------------------+
                                  | - Calls stylise_and_    |
                                  |   _compose(face, temp)  |
                                  | - Returns base64 PNG    |
                                  +-------------------------+
```

## Flow

1. User uploads a child's photo from the React UI.
2. The UI sends a `POST /api/personalize` request with the image as
   `multipart/form-data`.
3. FastAPI reads the file, crops the face region, loads the template illustration
   and calls the stylisation/composition function.
4. The composed image is encoded as base64 and returned as JSON.
5. The React UI renders the resulting personalised illustration in an `<img>` tag.
