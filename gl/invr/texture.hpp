#pragma once
#define GLEW_STATIC

#include <GL/glew.h>

#include "shader.hpp"

namespace invr {
    /**
     * Simplistic texture wrapper designed for drawing only. General purpose internal texbuffers
     * should still be done using the OpenGL API.
     */
    class Texture2D final {
        GLuint mHandle;
        int mWidth;
        int mHeight;

    public:
        Texture2D(const char* fileName);

        Texture2D(const Texture2D&) = delete;
        Texture2D& operator=(const Texture2D&) = delete;

        Texture2D(Texture2D&& other);
        Texture2D& operator=(Texture2D&& other);

        ~Texture2D();

        /**
         * Use this texture for drawing.
         */
        void use();

        /**
         * Bind this texture to a shader uniform under name.
         */
        void bindToShader(Shader& shader, const char* name);
    };
}
