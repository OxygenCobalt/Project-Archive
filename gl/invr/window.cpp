#define GLEW_STATIC

#include <GL/glew.h>
#include <GLFW/glfw3.h>
#include <stdexcept>

#include "window.hpp"

namespace invr {
    Window::Window(GLFWwindow* window, const unsigned int w, const unsigned int h) : glfwWindow(window), width(w), height(h) {}

    void assertValidWindow(const GLFWwindow* window) {
        if (!window) {
            // GLFW window was freed up, making this window instance invalid.
            throw std::runtime_error("This window instance is no longer valid.");
        }
    }

    bool Window::isRunning() const {
        return !glfwWindowShouldClose(getGLFWWindow());
    }

    void Window::fill(const float r, const float g, const float b) const {
        assertValidWindow(glfwWindow);

        glClearColor(r, g, b, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);    
    }

    void Window::flip() const {
        glfwSwapBuffers(getGLFWWindow());
    }

    GLFWwindow* Window::getGLFWWindow() const {
        assertValidWindow(glfwWindow);

        return glfwWindow;
    }

    void Window::quit() {
        glfwTerminate();
        glfwWindow = nullptr;
    }

    Window init(const unsigned int width, const unsigned int height) {
        glfwInit();

        // OpenGL version is 3.2
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);

        // We only want a context that supports new functionality
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);

        // Not resizable
        glfwWindowHint(GLFW_RESIZABLE, GL_FALSE);

        const auto window = glfwCreateWindow(width, height, "OpenGL", nullptr, nullptr);

        glfwMakeContextCurrent(window);

        glewExperimental = GL_TRUE;
        glewInit();
        
        glViewport(0, 0, width, height);

        return Window(window, width, height);
    }
}
