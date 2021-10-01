#pragma once

#include <glm/glm.hpp>

class Camera {
    glm::mat4 mProjMatrix;
    glm::mat4 mViewMatrix;
    glm::vec3 mPosition;
    glm::vec3 mRotation;

public:
    Camera(const float width, const float height);

    void move(const float dX, const float dY);
    void rotate(const float rX, const float rY);

    const glm::mat4& getView();
    const glm::mat4& getProj();
};