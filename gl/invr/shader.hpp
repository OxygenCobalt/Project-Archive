#pragma once
#define GLEW_STATIC

#include <string>
#include <GL/glew.h>
#include <glm/glm.hpp>

namespace invr {
    /*
    * Shortcut for a uniform handle
    */
    using Uniform = GLuint;

    /*
    * Wrapper around the OpenGL shader framework that enables
    * easy management and usage.
    * @author OxygenCobalt
    */
    class Shader final {
        GLuint mHandle;

    public:
        /*
         * Create a shader from two file names, one for the fragment and the other for the vertex shader
         */
        Shader(const std::string frag, const std::string vert);

        Shader(const Shader&) = delete;
        Shader& operator=(const Shader&) = delete;

        Shader(Shader&& other);
        Shader& operator=(Shader&& other);

        ~Shader();

        /**
         * Use this shader for drawing.
         */
        void use();

        /**
         * Add a vec2 attribute from vertex data.
         * @param spacing The spacing between data [e.g XY....XY -> 6]
         * @param offset The offset before the data starts [e.g ....XY -> 4]
         */
        void addVec2(const char* name, const size_t spacing, const size_t offset);

        /**
         * Add a vec3 attribute from vertex data.
         * @param spacing The spacing between data [e.g XY....XY -> 6]
         * @param offset The offset before the data starts [e.g ....XY -> 4]
         */
        void addVec3(const char* name, const size_t spacing, const size_t offset);

        /**
         * Get a uniform under name for this shader.
         * It is up to you to apply the correct values to this uniform.
         * @throws std::runtime_error When the uniform does not exist in the shader.
         */
        Uniform getUniform(const char* name) const;

        /**
         * Put an integer into this shader.
         */
        void putInt(const Uniform uniform, const int val);

        /**
         * Put a float into this shader.
         */
        void putFloat(const Uniform uniform, const float val);

        /**
         * Put a float vector into this shader.
         */
        void putVec(const Uniform uniform, const glm::vec3& val);

        /**
         * Put a integer vector into this shader.
         */
        void putIntVec(const Uniform uniform, const glm::ivec3& val);

        /**
         * Put a size-4 matrix into a this shader.
         */
        void putMat(const Uniform uniform, const glm::mat4& val);

        /**
         * Put an RGB color into this shader. This should be preferred over putVec since it only deals
         * with primitives.
         */
        void putColor(const Uniform uniform, const float r, const float g, const float b);
    };
}
