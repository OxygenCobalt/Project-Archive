#pragma once
#define GLEW_STATIC

#include <GL/glew.h>

#include "texture.hpp"
#include "shader.hpp"

namespace invr {
    /**
     * A wrapper around the OpenGL framebuffer.
     */
    class FrameBuffer final {
        GLuint mHandle;
        GLuint mTexBufferHandle;
        GLuint mRenderBufferHandle;

        size_t mWidth = 0;
        size_t mHeight = 0;

    public:
        FrameBuffer(size_t width, size_t height);

        FrameBuffer(const FrameBuffer&) = delete;
        FrameBuffer& operator=(const FrameBuffer&) = delete;

        FrameBuffer(FrameBuffer&& other);
        FrameBuffer& operator=(FrameBuffer&& other);

        ~FrameBuffer();

        /**
         * Use this framebuffer. After this is called, all draw operations will be done
         * on this framebuffer.
         */
        void use();

        /**
         * Drop this framebuffer. After this is called, all draw operations will be done
         * on the default framebuffer.
         */
        void drop();

        /**
         * Use the internal texture of this framebuffer for drawing.
         */
        void useTexture();

        /**
         * Bind this framebuffer to a corresponding shader uniform.
         */
        void bindToShader(Shader& shader, const char* name);
    };    
}
