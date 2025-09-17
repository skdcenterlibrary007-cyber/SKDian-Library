
# Library App - GitHub Ready

## How to use
1. Upload this repo to GitHub.
2. GitHub Actions will automatically build:
   - Windows EXE (`LibraryApp.exe`)
   - Android APK (`LibraryApp.apk`)
3. Download artifacts from Actions page once workflow completes.

## Change App Name
- Windows EXE: change `--name` in `.github/workflows/build-exe.yml`
- Android APK: change `"name"` and `"slug"` in `frontend/app.json` (Expo config)
