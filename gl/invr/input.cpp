#include <functional>
#include <glm/glm.hpp>
#include <GLFW/glfw3.h>

#include "input.hpp"

static std::function<void(double, double)> mouseCallback;

int isFocused = 0;
bool hasAddedGLFWCallback = false;

static void onMouseMove(GLFWwindow* window, double mouseX, double mouseY) {
    // Dont call if the window is not focused.
    if (isFocused) {
        mouseCallback(mouseX, mouseY);
    }
}

static void onFocusChange(GLFWwindow* window, int focus) {
    isFocused = focus;
}

namespace invr {
    void poll() {
        glfwPollEvents();
    }

    bool isKeyPressed(const Window& window, int key) {
        return glfwGetKey(window.getGLFWWindow(), key) == GLFW_PRESS;
    }

    void addMouseListener(const Window& window, std::function<void(double, double)> callback) {
        if (!hasAddedGLFWCallback) {
            glfwSetCursorPosCallback(window.getGLFWWindow(), onMouseMove);
            glfwSetWindowFocusCallback(window.getGLFWWindow(), onFocusChange);

            GLFWmousebuttonfun fun;

            hasAddedGLFWCallback = true;
        }

        mouseCallback = callback;
    }

    glm::vec<2, double> getCursorPosition(const Window& window) {
        double cursorX;
        double cursorY;

        glfwGetCursorPos(window.getGLFWWindow(), &cursorX, &cursorY);

        return glm::vec2(cursorX, cursorY);
    }

    void setCursorPosition(const Window& window, double x, double y) {
        glfwSetCursorPos(window.getGLFWWindow(), x, y);
    }
}
