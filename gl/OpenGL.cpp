#define GLEW_STATIC

#include <GL/glew.h>
#include <glm/glm.hpp>
#include <glm/gtc/matrix_transform.hpp>
#include <iostream>
#include <chrono>

#include "invr/window.hpp"
#include "invr/shader.hpp"
#include "invr/texture.hpp"
#include "invr/framebuffer.hpp"
#include "invr/vertex_array.hpp"
#include "invr/input.hpp"
#include "invr/camera.hpp"

#include "vertices.hpp"

int main() {
    auto window = invr::init(800, 600);

    auto t_start = std::chrono::high_resolution_clock::now();
    
    auto vertexQuad = invr::VertexArray(sizeof(quadVertices), quadVertices);
    auto vertexCube = invr::VertexArray(sizeof(cubeVertices), cubeVertices);

    // Create shader programs
    auto sceneShader = invr::Shader { "scene.vert", "scene.frag" };
    auto screenShader = invr::Shader { "screen.vert", "screen.frag" };

    vertexCube.use();

    sceneShader.addVec3("position", 8, 0);
    sceneShader.addVec3("color", 8, 3);
    sceneShader.addVec2("texCoord", 8, 6);

    vertexQuad.use();

    screenShader.addVec2("position", 4, 0);
    screenShader.addVec2("texCoord", 4, 2);

    // Load textures
    auto texCblt = invr::Texture2D("./res/textures/oxycblt.png");
    texCblt.bindToShader(sceneShader, "tex");

    auto framebuffer = invr::FrameBuffer(window.width, window.height);
    framebuffer.bindToShader(screenShader, "texFramebuffer");

    sceneShader.use();

    auto modelUni = sceneShader.getUniform("model");
    auto viewUni = sceneShader.getUniform("view");
    auto projUni = sceneShader.getUniform("proj");
    auto colorUni = sceneShader.getUniform("overrideColor");

    auto camera = Camera((float) window.width, (float) window.height);

    sceneShader.putMat(viewUni, camera.getView());
    sceneShader.putMat(projUni, camera.getProj());

    while (window.isRunning()) {
        
        // --- GAME LOGIC ---

        invr::poll();

        if (invr::isKeyPressed(window, GLFW_KEY_W)) {
            camera.move(0.0, 0.1f);
        } else if (invr::isKeyPressed(window, GLFW_KEY_A)) {
            camera.move(-0.1, 0.0f);
        } else if (invr::isKeyPressed(window, GLFW_KEY_S)) {
            camera.move(0.0, -0.1f);
        } else if (invr::isKeyPressed(window, GLFW_KEY_D)) {
            camera.move(0.1, 0.0f);
        }

        // --- DRAW LOGIC ---

        // Bind our framebuffer and draw 3D scene (spinning cube)
        sceneShader.use();
        framebuffer.use();
        texCblt.use();

        glEnable(GL_DEPTH_TEST);

        // Clear the screen to white
        window.fill(1.0f, 1.0f, 1.0f);

        // Calculate transformation
        auto time = std::chrono::duration_cast<std::chrono::duration<float>>(
            std::chrono::high_resolution_clock::now() - t_start
        ).count();
        
        auto model = glm::rotate(
            glm::mat4(1.0f),
            time * glm::radians(180.0f),
            {0.0f, 0.0f, 1.0f}
        );

        sceneShader.putMat(modelUni, model);
        sceneShader.putMat(viewUni, camera.getView());

        // Draw cube
        vertexCube.draw(0, 36);
        
        glEnable(GL_STENCIL_TEST);

        // Draw floor
        glStencilFunc(GL_ALWAYS, 1, 0xFF);
        glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE);
        glStencilMask(0xFF);
        glDepthMask(GL_FALSE);
        glClear(GL_STENCIL_BUFFER_BIT);

        vertexCube.draw(36, 6);

        // Draw cube reflection
        glStencilFunc(GL_EQUAL, 1, 0xFF);
        glStencilMask(0x00);
        glDepthMask(GL_TRUE);

        model = glm::scale(glm::translate(model, glm::vec3(0, 0, -1)), glm::vec3(1, 1, -1));
        sceneShader.putMat(modelUni, model);

        sceneShader.putVec(colorUni, glm::vec3(0.3f, 0.3f, 0.3f));
        vertexCube.draw(0, 36);
        sceneShader.putVec(colorUni, glm::vec3(1.0f, 1.0f, 1.0f));

        glDisable(GL_STENCIL_TEST);
        glDisable(GL_DEPTH_TEST);
        
        framebuffer.drop();

        // Draw the contents of our framebuffer
        framebuffer.useTexture();
        screenShader.use();
        vertexQuad.draw();

        window.flip();
    }

    window.quit();
    
    return 0;
}
