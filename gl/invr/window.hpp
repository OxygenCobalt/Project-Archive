#pragma once

#include <GLFW/glfw3.h>
#include <memory>

namespace invr {
    class Window {
        GLFWwindow* glfwWindow;

    public:
        const unsigned int width;
        const unsigned int height;

        Window(GLFWwindow* window, const unsigned int w, const unsigned int h);

        /*
         * Returns whether the event loop for this window should be ran
         */
        bool isRunning() const;

        /*
         * Fill this display with a single color
         */
        void fill(const float r, const float g, const float b) const;

        /*
         * Flip the buffers on this display.
         */
        void flip() const;

        /*
         * Quit this program and free all memory. Any calls made to this window after this will result in a runtime error.
         */
        void quit();

        /*
         * Get the glfw window
         */
        GLFWwindow* getGLFWWindow() const;
    };

    /**
     * Initialize the engine. This will return a window with the specified
     * width/height.
     */
    Window init(const unsigned int width, unsigned int height);
}
