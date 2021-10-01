#define GLEW_STATIC

#include <GL/glew.h>

namespace invr {
    /**
     * A wrapper around the OpenGL VertexArray.
     */
    class VertexArray final {
        GLuint mArrayHandle;
        GLuint mBufferHandle;
        size_t mVertexCount;

    public:
        VertexArray(const size_t vertCount, const float* vertices);

        VertexArray(const VertexArray&) = delete;
        VertexArray& operator=(const VertexArray&) = delete;

        VertexArray(VertexArray&& other);
        VertexArray& operator=(VertexArray&& other);

        ~VertexArray();

        /**
         * Use both the VAO and the VBO of this VertexArray.
         */
        void use();

        /**
         * Draw all of the vertices of this VertexArray. This automatically
         * uses the VAO.
         */
        void draw(const GLenum drawMode = GL_TRIANGLES);

        /**
         * Draw a [count] of verticies, starting from [first]. The drawMode
         * defaults to DRAW_TRIANGLES if not specified. This automatically
         * uses the VAO.
         */
        void draw(const size_t first, const size_t count);

        /**
         * Draw a [count] of verticies, starting from [first]. The drawMode
         * defaults to DRAW_TRIANGLES if not specified. This automatically
         * uses the VAO.
         */
        void draw(const GLenum drawMode, const size_t first, const size_t count);
    };
}
