const int octaves = 6;
vec2 random2(vec2 p) {
    return fract(vec2(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453123, 
                      sin(dot(p, vec2(269.5, 183.3))) * 43758.5453123));
}

// Value Noise function (adjusted to work with fbm1)
float noise(vec2 st) {
    vec2 i = floor(st);
    vec2 f = fract(st);

    vec2 u = f * f * (3.0 - 2.0 * f);

    return mix(mix(dot(random2(i + vec2(0.0, 0.0)), f - vec2(0.0, 0.0)),
                   dot(random2(i + vec2(1.0, 0.0)), f - vec2(1.0, 0.0)), u.x),
               mix(dot(random2(i + vec2(0.0, 1.0)), f - vec2(0.0, 1.0)),
                   dot(random2(i + vec2(1.0, 1.0)), f - vec2(1.0, 1.0)), u.x), u.y);
}

// fbm1 function adjusted for your existing pattern system
float fbm1(vec2 _st) {
    float v = 0.0;
    float a = 0.5;
    vec2 shift = vec2(100.0);
    mat2 rot = mat2(cos(0.5), sin(0.5),
                    -sin(0.5), cos(0.5));
    for (int i = 0; i < octaves; ++i) {
        v += a * noise(_st);
        _st = rot * _st * 2.0 + shift;
        a *= 0.4;
    }
    return v;
}

// Example pattern using fbm1 (existing pattern function)
float pattern(vec2 uv, float time, inout vec2 q, inout vec2 r) {

    q = vec2(fbm1(uv * 0.1 + vec2(0.0, 0.0)),
             fbm1(uv + vec2(5.2, 1.3)));

    r = vec2(fbm1(uv * 0.1 + 4.0 * q + vec2(1.7 - time / 2.0, 9.2)),
             fbm1(uv + 4.0 * q + vec2(8.3 - time / 2.0, 2.8)));

    vec2 s = vec2(fbm1(uv + 5.0 * r + vec2(21.7 - time / 2.0, 90.2)),
                  fbm1(uv * 0.05 + 5.0 * r + vec2(80.3 - time / 2.0, 20.8))) * 0.25;

    return fbm1(uv * 0.05 + 4.0 * s);
}


void main() {
    vec2 uv = texCoord * 2.0;

    // Calculate direction from UV to mouse position
    vec2 flowDir = normalize(_Mouse.xy*2.0- uv)*0.5;
    
    // Apply distortion based on direction and distance
    uv = uv + _Mouse.xy - flowDir * 0.5;

    vec2 q, r;
    float _pattern = pattern(uv, _Time * 0.5, q, r);

    vec3 colour = vec3(_pattern) * 2.0;
    colour.r -= dot(q, r) * 15.0;
    colour = mix(colour, vec3(pattern(r, _Time, q, r), dot(q, r) * 15.0, -0.1), 0.5);
    colour -= q.y * 1.5;
    colour = mix(colour, vec3(0.2, 0.2, 0.2), (clamp(q.x, -1.0, 0.0)) * 3.0);

    vec4 final = vec4(-colour + (abs(colour) * 2.0), 1.0 / length(q));

    FragColor = final;
}

