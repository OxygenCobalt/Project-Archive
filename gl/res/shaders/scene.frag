#version 330

in vec3 fragColor;
in vec2 fragTexCoord;
out vec4 outColor;

uniform sampler2D tex;

void main() {
    outColor = vec4(fragColor, 1.0) * texture(tex, fragTexCoord);
}