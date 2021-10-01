#define GLEW_STATIC

#include <utility>
#include <GL/glew.h>

#include "vertex_array.hpp"

namespace invr {
    VertexArray::VertexArray(const size_t vertSize, const float* vertices) : mVertexCount(vertSize / sizeof(float)) {
        // Create the VAO
        glGenVertexArrays(1, &mArrayHandle);

        // Create the buffer
        glGenBuffers(1, &mBufferHandle);
        glBindBuffer(GL_ARRAY_BUFFER, mBufferHandle);
        glBufferData(GL_ARRAY_BUFFER, vertSize, vertices, GL_STATIC_DRAW);
    }

    VertexArray::~VertexArray() {
        glDeleteVertexArrays(1, &mArrayHandle);
        glDeleteBuffers(1, &mBufferHandle);
    }

    VertexArray::VertexArray(VertexArray&& other) {
        *this = std::move(other);
    }

    VertexArray& VertexArray::operator=(VertexArray&& other) {
        glDeleteVertexArrays(1, &mArrayHandle);
        glDeleteBuffers(1, &mBufferHandle);
        
        mArrayHandle = other.mArrayHandle;
        mBufferHandle = other.mBufferHandle;
        mVertexCount = other.mVertexCount;

        other.mArrayHandle = 0;
        other.mBufferHandle = 0;
        other.mVertexCount = 0;

        return *this;
    }

    void VertexArray::use() {
        glBindVertexArray(mArrayHandle);
        glBindBuffer(GL_ARRAY_BUFFER, mBufferHandle);
    }

    void VertexArray::draw(const GLenum drawMode) {
        draw(drawMode, 0, mVertexCount);
    }

    void VertexArray::draw(const size_t first, const size_t count) {
        draw(GL_TRIANGLES, first, count);
    }

    void VertexArray::draw(const GLenum drawMode, const size_t first, const size_t count)  {
        glBindVertexArray(mArrayHandle);
        glDrawArrays(drawMode, first, count);
    }
}
