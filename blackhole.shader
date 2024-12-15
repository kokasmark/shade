float random (in vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))
                 * 43758.5453123);
}

// 2D Noise based on Morgan McGuire @morgan3d
// https://www.shadertoy.com/view/4dS3Wd
float randomNoise (in vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    // Four corners in 2D of a tile
    float a = random(i);
    float b = random(i + vec2(1.0, 0.0));
    float c = random(i + vec2(0.0, 1.0));
    float d = random(i + vec2(1.0, 1.0));

    // Smooth Interpolation

    // Cubic Hermine Curve.  Same as SmoothStep()
    vec2 u = f*f*(3.0-2.0*f);
    // u = smoothstep(0.,1.,f);

    // Mix 4 coorners percentages
    return mix(a, b, u.x) +
            (c - a)* u.y * (1.0 - u.x) +
            (d - b) * u.x * u.y;
}

// 3D rotation function
vec3 rotate3D(vec3 v, float phi, float theta) {
    mat3 rotX = mat3(
        1.0, 0.0, 0.0,
        0.0, cos(phi), -sin(phi),
        0.0, sin(phi), cos(phi)
    );
    
    mat3 rotY = mat3(
        cos(theta), 0.0, sin(theta),
        0.0, 1.0, 0.0,
        -sin(theta), 0.0, cos(theta)
    );

    return rotY * rotX * v;
}
vec3 quantizeColor(vec3 color, int levels) {
    float levelsFloat = float(levels);

    color = floor(color * levelsFloat) / levelsFloat;
    
    return color;
}
void main() {
    vec2 uv = gl_FragCoord.xy / vec2(1920.0, 1080.0);
    vec2 prop = vec2(1920.0/2, 1080.0/2) / 1920.0;
    vec2 uvc = prop * (2.0 * (uv - 0.5));
    
    vec4 col = vec4(0.12);

    float oneThird = 1.0 / 3.0;
    float root3 = sqrt(3.0);
    vec3 rayD = vec3(sqrt(1.0 - (oneThird * dot(uvc, uvc))), uvc.x / root3, uvc.y / root3);

    float phi = 0.05 * _Mouse.x ;
    float theta = -0.5 * _Mouse.y;

    float camCL = -5.0 * (0.2 * sin(_Time * 0.5) + 1.0);
    vec3 camC = camCL * vec3(1.0, 0.0, 0.0);

    rayD = rotate3D(rayD, phi, theta);
    camC = rotate3D(camC, phi, theta);

    vec3 lightDir = normalize(vec3(1.0, 0.0, -1.0));
    vec3 p = camC;

    float l = 0.0;
    float l2 = 0.0;

    float g = 0.008;
    float noiseFactor = 0.0;

    float blurStrength = 0.00025;
    float blurPhi = 0.0;
    float blurTheta = 0.0;

    for (int i = 0; i < 1000; i++) {
        l = length(p);
        l2 = (l * l) + 0.0001;

        rayD -= (g * p / (l2)) * 0.2;
        rayD = normalize(rayD);

        noiseFactor =0.5;

        p += rayD * (0.01 + (0.0025 * (noiseFactor - 0.5)));

        if (l < 0.1) {
            break;
        }

        if (abs(p.z * (l / 0.1)) < 0.05) {
            float rotAng = _Time + 1.0 / l;

            mat2 nrot;
            nrot[0] = vec2(cos(rotAng), -sin(rotAng));
            nrot[1] = vec2(sin(rotAng), cos(rotAng));

            col += 0.025 * randomNoise(nrot * (p.xy * 0.1) *100) * vec4(1.0, 0.77, 0.53, 1.0) / (l2 * l + 0.12);
        }
    }

    //col.rgb = quantizeColor(col.rgb,4);
    FragColor = col;
}
