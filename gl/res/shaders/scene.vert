#version 330

in vec3 position;
in vec3 color;
in vec2 texCoord;

out vec3 fragColor;
out vec2 fragTexCoord;

uniform mat4 model;
uniform mat4 view;
uniform mat4 proj;
uniform vec3 overrideColor;

void main()
{
    fragColor = overrideColor * color;
    fragTexCoord = texCoord;
    gl_Position = proj * view * model * vec4(position, 1.0);
}