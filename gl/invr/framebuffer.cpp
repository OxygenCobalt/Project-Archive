#define GLEW_STATIC

#include <stdexcept>
#include <GL/glew.h>

#include "framebuffer.hpp"

namespace invr {
    FrameBuffer::FrameBuffer(const size_t width, const size_t height) : mWidth(width), mHeight(height) {
        // Create and use the framebuffer right now
        glGenFramebuffers(1, &mHandle);

        use();

        // Create texture to hold color buffer. The abstraction isn't used here
        // since this is a fundamental component of the framebuffer that does not need
        // the external functionality of Texture2D.
        glGenTextures(1, &mTexBufferHandle);
        glBindTexture(GL_TEXTURE_2D, mTexBufferHandle);
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, nullptr);

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
        
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, mTexBufferHandle, 0);

        // Create Renderbuffer Object to hold depth and stencil buffers
        glGenRenderbuffers(1, &mRenderBufferHandle);
        glBindRenderbuffer(GL_RENDERBUFFER, mRenderBufferHandle);
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, mWidth, mHeight);
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, mRenderBufferHandle);

        // Finally check if the framebuffer has been built, if not, throw.
        if (glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) {
            throw std::runtime_error("Failed to create framebuffer.");
        }

        // Drop this framebuffer since it's done being configured
        drop();
    }

    FrameBuffer::FrameBuffer(FrameBuffer&& other) {
        *this = std::move(other);
    }

    FrameBuffer& FrameBuffer::operator=(FrameBuffer&& other) {
        glDeleteFramebuffers(1, &mHandle);
        glDeleteRenderbuffers(1, &mRenderBufferHandle);
        glDeleteTextures(1, &mTexBufferHandle);

        mTexBufferHandle = other.mTexBufferHandle;
        mHandle = other.mHandle;
        mRenderBufferHandle = other.mRenderBufferHandle;
        mWidth = other.mWidth;
        mHandle = other.mHeight;

        other.mHandle = 0;
        other.mTexBufferHandle = 0;
        other.mRenderBufferHandle = 0;
        other.mWidth = 0;
        other.mHeight = 0;

        return *this;
    }

    FrameBuffer::~FrameBuffer() {
        glDeleteFramebuffers(1, &mHandle);
        glDeleteRenderbuffers(1, &mRenderBufferHandle);
    }

    void FrameBuffer::use() {
        glBindFramebuffer(GL_FRAMEBUFFER, mHandle);
        glViewport(0, 0, mWidth, mHeight);
    }

    void FrameBuffer::drop() {
        glBindFramebuffer(GL_FRAMEBUFFER, 0);
    }

    void FrameBuffer::useTexture() {
        glBindTexture(GL_TEXTURE_2D, mTexBufferHandle);
    }

    void FrameBuffer::bindToShader(Shader& shader, const char* name) {
        shader.putInt(shader.getUniform(name), 0);
    }
}
