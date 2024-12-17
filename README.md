# Image Restorer Frontend

A Vue-based project featuring Vuetify, tailwind CSS.

## File Structure

This is a typical Vue 3 framework project, which includes routing functionality. Below is an explanation of the main file directory.

```bash
Image Restorer Frontend/
│
├── public/                     # Public files
│   ├── images/                 # Folder for image assets
│   └── svgs/                   # Folder for SVG assets
│
├── src/                        # Source code files
│   ├── assets/                 # Static assets (CSS, images, fonts, etc.)
│   │   └── tailwind.css        # Tailwind CSS configuration file
│   │
│   ├── components/             # Reusable components 
│   │   
│   │
│   ├── views/                  # Page components 
│   │   
│   │
│   ├── router/                 # Routing configuration
│   │   └── index.js            # File that handles route definitions
│   │
│   ├── App.vue                 # Root component (top-level component)
│   ├── main.js                 # Entry file for initializing the Vue instance
│   
│
├── package.json                # Project dependencies, scripts, and metadata
└── index.html                  # Main HTML file (entry point)
```

## Prerequisites

Ensure you have the following installed before starting:

- **Node.js** (v16 or later recommended)  
  [Download Node.js](https://nodejs.org/)  
  Verify installation:  

  ```bash
  node -v
  npm -v
  ```



## Getting Started

To set up and run this project locally, follow these steps:

1. **Clone the Repository**

   Clone the repository from GitHub to your local machine:

   ```bash
   git clone https://github.com/no-tomatoes-tonight-or-id-scream/image-restorer-frontend.git
   ```

2. **Install Dependencies**

    In addition to the Vue base dependencies, this project uses the following key dependencies:

    - **[@element-plus/icons-vue](https://github.com/element-plus/element-plus-icons)**: Element Plus icons for Vue 3.
    - **[axios](https://axios-http.com/)**: A promise-based HTTP client for the browser and Node.js.
    - **[daisyui](https://daisyui.com/)**: A plugin for Tailwind CSS that provides a set of accessible UI components.
    - **[element-plus](https://element-plus.org/)**: A Vue 3 based component library for developers, designers, and product managers.
    - **[tailwindcss](https://tailwindcss.com/)**: A utility-first CSS framework for rapid UI development.
    - **[vue-router](https://router.vuejs.org/)**: The official router for Vue.js for managing page navigation.
    - **[vuetify](https://vuetifyjs.com/)**: A Material Design component framework for Vue.js.
    - **[winterx/color4bg](https://github.com/winterx/color4bg.js)**: A Super easily generate dynamic, abstract, and visually stunning background images for your web pages based on WebGL and JavaScript. High performance.
   
  You can use the `npm list` in the project directory to see if these dependencies are already installed.
    
  Install all required dependencies using npm:

  Navigate to the project directory where the `package.json` file is located and run the following command to install the necessary dependencies:
  ```bash
  npm install
  ```
   Or use the following command when you check for the lack of a particular dependency
  ```bash
  npm install vue-icon
  npm install vue-router
  npm install vuetify
  ```

3. **Run the Project**

   Start the development server:

   ```bash
   npm run dev
   ```

​	By default, the application will be accessible at `http://localhost:5173`

## Support

- If you have any questions or encounter issues, feel free to open an issue on GitHub.
