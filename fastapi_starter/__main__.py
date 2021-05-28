import uvicorn
import varname

import fastapi_starter.app

if __name__ == "__main__":
    module_path = varname.nameof(fastapi_starter.app, vars_only=False)
    app_name = varname.nameof(fastapi_starter.app.app)
    uvicorn.run(f"{module_path}:{app_name}", host="0.0.0.0", port=8000, reload=True)
