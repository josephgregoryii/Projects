class Camera
{
  public:
    double          near, far;
    double          angle;
    double          position[3];
    double          focus[3];
    double          up[3];

    double O[3];
    double U[3];
    double V[3];
    double W[3];

    Matrix          CameraTransform;
    Matrix          ViewTransform;
    Matrix          DeviceTransform;

    void            ViewTransform(void) {;};
    void            CameraTransform(void) {;};
    void            DeviceTransform(void) {;};
};

void
Camera::ViewTransform()
{

    ViewTransform.A[0][0] = 1 / tan(angle/2); 
    ViewTransform.A[0][1] = 0;
    ViewTransform.A[0][2] = 0;
    ViewTransform.A[0][3] = 0;
    ViewTransform.A[1][0] = 0;
    ViewTransform.A[1][1] = 1 / tan(angle/2); 
    ViewTransform.A[1][2] = 0;
    ViewTransform.A[1][3] = 0;
    ViewTransform.A[2][0] = 0;
    ViewTransform.A[2][1] = 0;
    ViewTransform.A[2][2] = (far + near) / (far - near); 
    ViewTransform.A[2][3] = -1;
    ViewTransform.A[3][0] = 0;
    ViewTransform.A[3][1] = 0;
    ViewTransform.A[3][2] = (2 * far * near) / (far - near);
    ViewTransform.A[3][3] = 0;
}


void
Camera::CameraTransform()
{
    double o_min_focus[3];
    double total = 0.0;
    double vtx_u;
    double vtx_v;
    double vtx_w;

    for (int i = 0; i < 3; i++)
    {
        O[i]           = position[i];
        o_min_focus[i] = position[i] - focus[i];
    }

    //vector 1
    std::vector<double> v1 = crossProduct(up, o_min_focus)
    for (int i = 0; i < 3; i++)
    {
        U[i]         = v1[i];
        double temp  = v1[i];
        total        += temp * temp;
    }

    vtx_u = total;
    total = 0.0;//reset total, using later

    for (int i = 0; i < 3; i++)
    {
        if (fabs(vtx_u) < 0.00001)
            U[i] = 0;
        else
            U[i] = U[i] / sqrt(vtx_u);
    }


    //vector 2
    std::vector<double> v2 = crossProduct(o_min_focus, U)
    for (int i = 0; i < 3; i++)
    {
        V[i] = v2[i];
        double temp  = v2[i];
        total += temp * temp;
    }

    vtx_v= total;
    total = 0.0

    for (int i = 0; i < 3; i++)
    {
        if (fabs(vtx_v) < 0.00001)
            V[i] = 0;
        else
            V[i] = V[i] / sqrt(vtx_v);
    }

    for ( int i = 0; i < 3; i++)
    {
       W[i] = o_min_focus[i];
       double temp = o_min_focus[i];
       total = temp * temp;
    }
    vtx_w = total;
    total = 0.0;

    for (int i = 0; i < 3; i++)
    {
        if (fabs(vtx_w) < 0.00001)
            W[i] = 0;
        else
            W[i] = W[i] / sqrt(vtx_w);
    }

    double t[3];
    for(int i = 0; i < 3; i++)
    {
        t[i] = 0 - O[i];
    }

    for(int i = 0; i < 3; i++)
    {
        for(int j = 0; j < 1; j++)
        {
            CameraTransform.A[i][j]   = U[i];// A[i][0] U
            CameraTransform.A[i][j+1] = V[i];// A[i][1] V
            CameraTransform.A[i][j+2] = W[i];// A[i][2] W
            CameraTransform.A[i][j+3] = 0;   // A[i][3] 0

        }
    }
    CameraTransform.A[3][0] = dotProduct(U, t, 3);
    CameraTransform.A[3][1] = dotProduct(V, t, 3);
    CameraTransform.A[3][2] = dotProduct(W, t, 3);
    CameraTransform.A[3][3] = 1;
    


}

void
Camera::DeviceTransform(Screen s) 
{
    DeviceTransform.A[0][0] = s.width / 2; 
    DeviceTransform.A[0][1] = 0;
    DeviceTransform.A[0][2] = 0;
    DeviceTransform.A[0][3] = 0;
    DeviceTransform.A[1][0] = 0;
    DeviceTransform.A[1][1] = s.width / 2; 
    DeviceTransform.A[1][2] = 0;
    DeviceTransform.A[1][3] = 0;
    DeviceTransform.A[2][0] = 0;
    DeviceTransform.A[2][1] = 0;
    DeviceTransform.A[2][2] = 1 
    DeviceTransform.A[2][3] = 0;
    DeviceTransform.A[3][0] = s.width / 2;
    DeviceTransform.A[3][1] = s.width / 2;
    DeviceTransform.A[3][2] = 0 
    DeviceTransform.A[3][3] = 1;

}



double SineParameterize(int curFrame, int nFrames, int ramp)
{
    int nNonRamp = nFrames-2*ramp;
    double height = 1./(nNonRamp + 4*ramp/M_PI);
    if (curFrame < ramp)
    {
        double factor = 2*height*ramp/M_PI;
        double eval = cos(M_PI/2*((double)curFrame)/ramp);
        return (1.-eval)*factor;
    }
    else if (curFrame > nFrames-ramp)
    {
        int amount_left = nFrames-curFrame;
        double factor = 2*height*ramp/M_PI;
        double eval =cos(M_PI/2*((double)amount_left/ramp));
        return 1. - (1-eval)*factor;
    }
    double amount_in_quad = ((double)curFrame-ramp);
    double quad_part = amount_in_quad*height;
    double curve_part = height*(2*ramp)/M_PI;
    return quad_part+curve_part;
}

Camera
GetCamera(int frame, int nframes)
{
    double t = SineParameterize(frame, nframes, nframes/10);
    Camera c;
    c.near = 5;
    c.far = 200;
    c.angle = M_PI/6;
    c.position[0] = 40*sin(2*M_PI*t);
    c.position[1] = 40*cos(2*M_PI*t);
    c.position[2] = 40;
    c.focus[0] = 0;
    c.focus[1] = 0;
    c.focus[2] = 0;
    c.up[0] = 0;
    c.up[1] = 1;
    c.up[2] = 0;
    return c;
}
