#pragma once

#include <functional>
#include <glm/glm.hpp>
#include "window.hpp"

namespace invr {
    void poll();
    bool isKeyPressed(const Window& window, int key);
    void addMouseListener(const Window& window, std::function<void(double, double)> callback);
    glm::vec<2, double> getCursorPosition(const Window& window);
    void setCursorPosition(const Window& window, double x, double y);
}