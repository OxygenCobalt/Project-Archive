#version 330

in vec2 fragTexCoord;
out vec4 outColor;

uniform sampler2D texFramebuffer;

void main() {
    outColor = texture(texFramebuffer, fragTexCoord);
}

