#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>

#include "camera.hpp"

const glm::mat4 baseViewMatrix = glm::lookAt(
    glm::vec3(0.0f, 2.5f, 1.5f),
    glm::vec3(0.0f, 0.0f, 0.0f),
    glm::vec3(0.0f, 0.0f, 1.0f)
);


Camera::Camera(const float width, const float height) : mPosition(), mRotation() {
    mViewMatrix = baseViewMatrix;
    
    mProjMatrix = glm::perspective(
        glm::radians(45.0f), width / height, 1.0f, 10.0f
    );
}

void Camera::move(const float dX, const float dY) {
    mPosition.x += dX;
    mPosition.y += dY;

    mViewMatrix = glm::translate(baseViewMatrix, mPosition);
}

void Camera::rotate(const float rX, const float rY) {
    mRotation.x += rX;
    mRotation.y += rY;

    mViewMatrix = glm::rotate(mViewMatrix, glm::radians(mRotation.x), {1, 0, 0});
    mViewMatrix = glm::rotate(mViewMatrix, glm::radians(mRotation.y), {0, 1, 0});
}

const glm::mat4& Camera::getView() {
    return mViewMatrix;
}

const glm::mat4& Camera::getProj() {
    return mProjMatrix;
}
