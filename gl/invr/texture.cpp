#define GLEW_STATIC

#include <iostream>
#include <utility>
#include <GL/glew.h>
#include <SOIL/SOIL.h>

#include "texture.hpp"
#include "shader.hpp"

namespace invr {
    Texture2D::Texture2D(const char* fileName) {
        glGenTextures(1, &mHandle);
        glActiveTexture(GL_TEXTURE0);
        use();

        auto image = SOIL_load_image(fileName, &mWidth, &mHeight, 0, SOIL_LOAD_RGBA);

        if (!image) {
            // TODO: Add a placeholder of some kind
            std::cerr << "Unable to load texture " << std::string(fileName) << std::endl;
        }

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, mWidth, mHeight, 0, GL_RGBA, GL_UNSIGNED_BYTE, image);
        SOIL_free_image_data(image);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);

        glGenerateMipmap(GL_TEXTURE_2D);
    }

    Texture2D::Texture2D(Texture2D&& other) {
        *this = std::move(other);
    }

    Texture2D& Texture2D::operator=(Texture2D&& other) {
        glDeleteTextures(1, &mHandle);

        mHandle = other.mHandle;
        mWidth = other.mWidth;
        mHeight = other.mHeight;

        other.mHandle = 0;
        other.mWidth = 0;
        other.mHeight = 0;
        
        return *this;
    }

    Texture2D::~Texture2D() {
        glDeleteTextures(1, &mHandle);

        mHandle = 0;
        mWidth = 0;
        mHeight = 0;
    }

    void Texture2D::use() {
        glBindTexture(GL_TEXTURE_2D, mHandle);
    }

    void Texture2D::bindToShader(Shader& shader, const char* name) {
        shader.putInt(shader.getUniform(name), 0);
    }
}
