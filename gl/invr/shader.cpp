#define GLEW_STATIC

#include <iostream>
#include <cstdio>
#include <stdexcept>
#include <string>
#include <sstream>
#include <fstream>

#include <GL/glew.h>
#include <glm/glm.hpp>
#include <glm/gtc/type_ptr.hpp>

#include "shader.hpp"

// All shaders should be in this path
constexpr const char* SHADER_PATH = "./res/shaders/";

// Build a new shader given a name and a type.
int newShader(const std::string path, const GLenum type) {
    const auto with_dir = SHADER_PATH + path;

    auto shaderFile = std::ifstream {
        with_dir
    };

    if (!shaderFile.is_open()) {
        throw std::runtime_error("Unable to open shader file " + path);
    }

    auto ss = std::ostringstream();
    ss << shaderFile.rdbuf();

    auto source_str = ss.str();
    GLchar *source = source_str.data();

    // Now build and compile the shader
    const auto shaderHandle = glCreateShader(type);
    glShaderSource(shaderHandle, 1, &source, nullptr);
    glCompileShader(shaderHandle);

    // Check for success, throw if it compiling failed with the log.
    GLint success;
    glGetShaderiv(shaderHandle, GL_COMPILE_STATUS, &success);

    if (!success) {
        GLchar log[512];
        glGetShaderInfoLog(shaderHandle, 512, nullptr, log);

        throw std::runtime_error("Unable to load shader " + path + ": " + std::string(log));
    }
 
    return shaderHandle;
}

namespace invr {
    Shader::Shader(const std::string vert, const std::string frag) {
        mHandle = glCreateProgram();

        auto vertShader = newShader(vert, GL_VERTEX_SHADER);
        auto fragShader = newShader(frag, GL_FRAGMENT_SHADER);
    
        glAttachShader(mHandle, vertShader);
        glAttachShader(mHandle, fragShader);
        glBindFragDataLocation(mHandle, 0, "outColor");

        glDeleteShader(vertShader);
        glDeleteShader(fragShader);

        glLinkProgram(mHandle);
    }

    Shader::Shader(Shader&& other) {
        *this = std::move(other);
    }

    Shader& Shader::operator=(Shader &&other) {
        glDeleteProgram(mHandle);

        mHandle = other.mHandle;
        other.mHandle = 0;

        return *this;
    }

    Shader::~Shader() {
        glDeleteProgram(mHandle);
    }

    void Shader::use() {
        glUseProgram(mHandle);
    }

    void Shader::addVec2(const char* name, const size_t spacing, const size_t offset) {
        auto attrib = glGetAttribLocation(mHandle, name);
        
        glVertexAttribPointer(
            attrib, 2, GL_FLOAT, GL_FALSE,
            spacing * sizeof(float), (const void*) (offset * sizeof(float))
        );

        glEnableVertexAttribArray(attrib);    
    }

    void Shader::addVec3(const char* name, const size_t spacing, const size_t offset) {
        auto attrib = glGetAttribLocation(mHandle, name);

        glVertexAttribPointer(
            attrib, 3, GL_FLOAT, GL_FALSE,
            spacing * sizeof(float), (const void*) (offset * sizeof(float)
        ));
        
        glEnableVertexAttribArray(attrib);        
    }

    Uniform Shader::getUniform(const char* name) const {
        auto uniform = glGetUniformLocation(mHandle, name);

        // Invalid uniforms will return -1, so we check for this to prevent frustrating errors
        if (uniform == -1) {
            throw std::runtime_error(
                "The uniform " + std::string(name) + " does not exist in this shader."
            );
        }

        return uniform;
    }

    void Shader::putInt(const Uniform uniform, int val) {
        glUniform1i(uniform, val);
    }

    void Shader::putFloat(const Uniform uniform, float val) {
        glUniform1f(uniform, val);
    }

    void Shader::putVec(const Uniform uniform, const glm::vec3& vec) {
        glUniform3fv(uniform, 1, glm::value_ptr(vec));
    }

    void Shader::putIntVec(const Uniform uniform, const glm::ivec3& vec) {
        glUniform3iv(uniform, 1, glm::value_ptr(vec));
    }

    void Shader::putMat(const Uniform uniform, const glm::mat4& mat) {
        glUniformMatrix4fv(uniform, 1, GL_FALSE, glm::value_ptr(mat));
    }

    void Shader::putColor(const Uniform uniform, const float r, const float g, const float b) {
        float color[] = {r, g, b};
        glUniform3fv(uniform, 1, color);
    }
}
