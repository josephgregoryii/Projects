#include <vtkPointData.h>
#include <vtkPolyData.h>
#include <vtkPolyDataReader.h>
#include <vtkPoints.h>
#include <vtkUnsignedCharArray.h>
#include <vtkFloatArray.h>
#include <vtkCellArray.h>
#include <vtkDoubleArray.h>
#include <iostream>
#include <sstream>
#include <vtkDataSet.h>
#include <vtkImageData.h>
#include <vtkPNGWriter.h>

using std::cerr;
using std::endl;


class Screen
{
    public:
        unsigned char *buffer;
        double *zBuffer;
        int width, height;

        void setZBuffer()
        {
            zBuffer = new double[width*height];

            for (int i = 0; i < width * height; i++)
            {
                zBuffer[i] = -1.0;
            }
        }
};

class Triangle
{
  public:
      double         X[3];
      double         Y[3];
      double         Z[3];
      double         color[3][3];
      Screen         screen;
};



class Matrix
{
    public:
        double A[4][4];

        void TransformPoint(const double *ptIn, double *ptOut);
        static Matrix ComposeMatrices(const Matrix &, const Matrix &);
        void Print(ostream &o);
};

double ceil_441(double f) {
    return ceil(f-0.00001);
}

double floor_441(double f) {
    return floor(f+0.00001);
}

double dotProduct(double array1[], double array2[], int length)
{
    double product = 0;
    for (int i=0; i < length; i++) {
        product += (array1[i] * array2[i]);
    }
    return product;
}



std::vector<double> crossProduct(double *a, double *b)
{
    std::vector<double> product(3);
    product[0] = (a[1] * b[2]) - (a[2] * b[1]);
    product[1] = (a[2] * b[0]) - (a[0] * b[2]);
    product[2] = (a[0] * b[1]) - (a[1] * b[0]);

    return product;
}



void Matrix::Print(ostream &o)
{
    for (int i = 0 ; i < 4 ; i++)
    {
        char str[256];
        sprintf(str, "(%.7f %.7f %.7f %.7f)\n", A[i][0], A[i][1], A[i][2], A[i][3]);
        o << str;
    }
}

Matrix Matrix::ComposeMatrices(const Matrix &M1, const Matrix &M2)
{
    Matrix rv;
    for (int i = 0 ; i < 4 ; i++)
        for (int j = 0 ; j < 4 ; j++)
        {
            rv.A[i][j] = 0;
            for (int k = 0 ; k < 4 ; k++)
                rv.A[i][j] += M1.A[i][k]*M2.A[k][j];
        }

    return rv;
}

void Matrix::TransformPoint(const double *ptIn, double *ptOut)
{
    ptOut[0] = ptIn[0]*A[0][0]
             + ptIn[1]*A[1][0]
             + ptIn[2]*A[2][0]
             + ptIn[3]*A[3][0];
    ptOut[1] = ptIn[0]*A[0][1]
             + ptIn[1]*A[1][1]
             + ptIn[2]*A[2][1]
             + ptIn[3]*A[3][1];
    ptOut[2] = ptIn[0]*A[0][2]
             + ptIn[1]*A[1][2]
             + ptIn[2]*A[2][2]
             + ptIn[3]*A[3][2];
    ptOut[3] = ptIn[0]*A[0][3]
             + ptIn[1]*A[1][3]
             + ptIn[2]*A[2][3]
             + ptIn[3]*A[3][3];
}

class Camera
{
    public:
        double near, far;
        double angle;
        double position[3];
        double focus[3];
        double up[3];

        double O[3];
        double v1[3];
        double v2[3];
        double v3[3];

        Matrix _CameraTransform;
        Matrix _ViewTransform;
        Matrix _DeviceTransform;

        void printCamera();
        void CameraTransform();
        void ViewTransform();
        void DeviceTransform(Screen s);
};

Screen InitializeScreen(unsigned char *buffer, int width, int height)
{
    Screen screen;
    screen.buffer = buffer;
    screen.width = width;
    screen.height = height;
    screen.setZBuffer();

    // initialize the buffer to black
    int npixels = width*height;
    for (int i = 0 ; i < npixels*3 ; i++)
        screen.buffer[i] = 0;

    return screen;
}

void
Camera::printCamera()
{
    cout << "position: (" << position[0] << " " << position[1] << " " << position[2] << ")\n";
    cout << "focus: (" << focus[0] << " " << focus[1] << " " << focus[2] << ")\n";
    cout << "up: (" << up[0] << " " << up[1] << " " << up[2] << ")\n\n";
}

void
Camera::CameraTransform()
{
    double total;
    double v1_dub;
    double v2_dub;
    double v3_dub;

    for (int i = 0; i < 3; i++) {
        O[i] = position[i];
    }

    double O_sub_focus[3];
    for (int i = 0; i < 3; i++) {
        O_sub_focus[i] = O[i] - focus[i];
    }

    std::vector<double> vect1 = crossProduct(up, O_sub_focus);
    for (int i = 0; i < 3; i++) {
        v1[i] = vect1[i];
    }

    total = 0.0;
    for (int i = 0; i < 3; i++) {
        double temp = v1[i];
        total += temp * temp;
    }

    v1_dub = total;
    for (int i = 0; i < 3; i++) {
        if (fabs(v1_dub) < 0.00001)
            v1[i] = 0;
        else
            v1[i] = v1[i] / sqrt(v1_dub);
    }

    std::vector<double> vect2 = crossProduct(O_sub_focus, v1);
    for (int i = 0; i < 3; i++) {
        v2[i] = vect2[i];
    }
    total = 0.0;
    for (int i = 0; i < 3; i++) {
        double temp = v2[i];
        total += temp * temp;
    }
    v2_dub = total;
    for (int i = 0; i < 3; i++) {
        if (fabs(v2_dub) < 0.00001)
            v2[i] = 0;
        else
            v2[i] = v2[i] / sqrt(v2_dub);
    }


    for (int i = 0; i < 3; i++) {
        v3[i] = O_sub_focus[i];
    }
    total = 0.0;
    for (int i = 0; i < 3; i++) {
        double temp = v3[i];
        total += temp * temp;
    }
    v3_dub = total;
    for (int i = 0; i < 3; i++) {
        if (fabs(v3_dub) < 0.00001) {
            v3[i] = 0;
        }
        else {
            v3[i] = v3[i] / sqrt(v3_dub);
        }
    }

    double t[3];
    t[0] = 0 - O[0];
    t[1] = 0 - O[1];
    t[2] = 0 - O[2];

    _CameraTransform.A[0][0] = v1[0];
    _CameraTransform.A[0][1] = v2[0];
    _CameraTransform.A[0][2] = v3[0];
    _CameraTransform.A[0][3] = 0;
    _CameraTransform.A[1][0] = v1[1];
    _CameraTransform.A[1][1] = v2[1];
    _CameraTransform.A[1][2] = v3[1];
    _CameraTransform.A[1][3] = 0;
    _CameraTransform.A[2][0] = v1[2];
    _CameraTransform.A[2][1] = v2[2];
    _CameraTransform.A[2][2] = v3[2];
    _CameraTransform.A[2][3] = 0;
    _CameraTransform.A[3][0] = dotProduct(v1, t, 3);
    _CameraTransform.A[3][1] = dotProduct(v2, t, 3);
    _CameraTransform.A[3][2] = dotProduct(v3, t, 3);
    _CameraTransform.A[3][3] = 1;

}

void
Camera::ViewTransform()
{
    _ViewTransform.A[0][0] = 1 / tan(angle/2);
    _ViewTransform.A[0][1] = 0;
    _ViewTransform.A[0][2] = 0;
    _ViewTransform.A[0][3] = 0;
    _ViewTransform.A[1][0] = 0;
    _ViewTransform.A[1][1] = 1 / tan(angle/2);
    _ViewTransform.A[1][2] = 0;
    _ViewTransform.A[1][3] = 0;
    _ViewTransform.A[2][0] = 0;
    _ViewTransform.A[2][1] = 0;
    _ViewTransform.A[2][2] = (far + near) / (far - near);
    _ViewTransform.A[2][3] = -1;
    _ViewTransform.A[3][0] = 0;
    _ViewTransform.A[3][1] = 0;
    _ViewTransform.A[3][2] = (2 * far * near) / (far - near);
    _ViewTransform.A[3][3] = 0;

}

void
Camera::DeviceTransform(Screen s)
{
    _DeviceTransform.A[0][0] = s.width / 2;
    _DeviceTransform.A[0][1] = 0;
    _DeviceTransform.A[0][2] = 0;
    _DeviceTransform.A[0][3] = 0;
    _DeviceTransform.A[1][0] = 0;
    _DeviceTransform.A[1][1] = s.width / 2;
    _DeviceTransform.A[1][2] = 0;
    _DeviceTransform.A[1][3] = 0;
    _DeviceTransform.A[2][0] = 0;
    _DeviceTransform.A[2][1] = 0;
    _DeviceTransform.A[2][2] = 1;
    _DeviceTransform.A[2][3] = 0;
    _DeviceTransform.A[3][0] = s.width / 2;
    _DeviceTransform.A[3][1] = s.width / 2;
    _DeviceTransform.A[3][2] = 0;
    _DeviceTransform.A[3][3] = 1;

}

double
SineParameterize(int curFrame, int nFrames, int ramp)
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
        double eval = cos(M_PI/2*((double)amount_left/ramp));
        return 1. - (1-eval)*factor;
    }
    double amount_in_quad = ((double)curFrame-ramp);
    double quad_part = amount_in_quad*height;
    double curve_part = height*(2*ramp)/M_PI;
    return quad_part+curve_part;
}

Camera GetCamera(int frame, int nframes)
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

void RasterizeGoingUpTriangle(Triangle triangle, unsigned char *buffer, int width, int height, double* zVals){

  double bleftX, bleftY, bleftZ; //base left
  double brightX, brightY, brightZ; //base right
  double topX, topY, topZ; //top of triangle
  double bleft_red, bleft_green, bleft_blue; //base left colors
  double bright_red, bright_green, bright_blue; //base right colors
  double topRed, topGreen, topBlue; //top colors
  double cur_leftRed, cur_leftGreen, cur_leftBlue; //current left colors
  double cur_rightRed, cur_rightGreen, cur_rightBlue; //current right colors
  double cur_red, cur_green, cur_blue; //current colors


  if(triangle.Y[0] == triangle.Y[1]){
    brightY = triangle.Y[0];
    bleftY  = triangle.Y[0];
    if(triangle.X[0] < triangle.X[1]){
      bleftX     = triangle.X[0];
      bleftZ     = triangle.Z[0];
      bleft_red   = triangle.color[0][0];
      bleft_green = triangle.color[0][1];
      bleft_blue  = triangle.color[0][2];

      brightX     = triangle.X[1];
      brightZ     = triangle.Z[1];
      bright_red   = triangle.color[1][0];
      bright_green = triangle.color[1][1];
      bright_blue  = triangle.color[1][2];
    }
    else{
      bleftX  = triangle.X[1];
      bleftZ  = triangle.Z[1];
      bleft_red   = triangle.color[1][0];
      bleft_green = triangle.color[1][1];
      bleft_blue  = triangle.color[1][2];

      brightX = triangle.X[0];
      brightZ = triangle.Z[0];
      bright_red   = triangle.color[0][0];
      bright_green = triangle.color[0][1];
      bright_blue  = triangle.color[0][2];
    }
    topX = triangle.X[2];
    topY = triangle.Y[2];
    topZ = triangle.Z[2];
    topRed   = triangle.color[2][0];
    topGreen = triangle.color[2][1];
    topBlue  = triangle.color[2][2];
  }
  else if(triangle.Y[0] == triangle.Y[2]){
    brightY = triangle.Y[0];
    bleftY  = triangle.Y[0];
    if(triangle.X[0] < triangle.X[2]){
      bleftX  = triangle.X[0];
      bleftZ  = triangle.Z[0];
      bleft_red   = triangle.color[0][0];
      bleft_green = triangle.color[0][1];
      bleft_blue  = triangle.color[0][2];

      brightX = triangle.X[2];
      brightZ = triangle.Z[2];
      bright_red   = triangle.color[2][0];
      bright_green = triangle.color[2][1];
      bright_blue  = triangle.color[2][2];
    }
    else{
      bleftX  = triangle.X[2];
      bleftZ  = triangle.Z[2];
      bleft_red   = triangle.color[2][0];
      bleft_green = triangle.color[2][1];
      bleft_blue  = triangle.color[2][2];

      brightX = triangle.X[0];
      brightZ = triangle.Z[0];
      bright_red   = triangle.color[0][0];
      bright_green = triangle.color[0][1];
      bright_blue  = triangle.color[0][2];
    }
    topX = triangle.X[1];
    topY = triangle.Y[1];
    topZ = triangle.Z[1];
    topRed   = triangle.color[1][0];
    topGreen = triangle.color[1][1];
    topBlue  = triangle.color[1][2];
  }
  else{
    brightY = triangle.Y[1];
    bleftY  = triangle.Y[1];
    if(triangle.X[1] < triangle.X[2]){
      bleftX  = triangle.X[1];
      bleftZ  = triangle.Z[1];
      bleft_red   = triangle.color[1][0];
      bleft_green = triangle.color[1][1];
      bleft_blue  = triangle.color[1][2];

      brightX = triangle.X[2];
      brightZ = triangle.Z[2];
      bright_red   = triangle.color[2][0];
      bright_green = triangle.color[2][1];
      bright_blue  = triangle.color[2][2];
    }
    else{
      bleftX  = triangle.X[2];
      bleftZ  = triangle.Z[2];
      bleft_red   = triangle.color[2][0];
      bleft_green = triangle.color[2][1];
      bleft_blue  = triangle.color[2][2];

      brightX = triangle.X[1];
      brightZ = triangle.Z[1];
      bright_red   = triangle.color[1][0];
      bright_green = triangle.color[1][1];
      bright_blue  = triangle.color[1][2];
    }
    topX = triangle.X[0];
    topY = triangle.Y[0];
    topZ = triangle.Z[0];
    topRed   = triangle.color[0][0];
    topGreen = triangle.color[0][1];
    topBlue  = triangle.color[0][2];
  }

  int ymin = ((bleftY < 0) ? 0 : ceil_441(bleftY));
  int ymax = ((topY >= height) ? (height - 1) : floor_441(topY));


  double* l_slope ;
  double* r_slope;

  if(topX == bleftX){
    l_slope = NULL;
  }
  else{
    double val1 = (topY - bleftY)/(topX - bleftX);
    l_slope = &val1;
  }
  if(topX == brightX){
    r_slope = NULL;
  }
  else{
    double val2 = (brightY - topY)/(brightX - topX);
    r_slope = &val2;
  }

  for(int i = ymin; i <= ymax; i++){
    int r_bound, l_bound, leftZ, rightZ;
    double cur_leftX, cur_rightX, cur_leftZ, cur_rightZ, cur_Z;

    cur_leftX = ((l_slope != NULL) ? bleftX + (((double) i) - bleftY)/(*l_slope) : bleftX);
    l_bound = ((cur_leftX < 0) ? 0 : ceil_441(cur_leftX));

    cur_rightX = ((r_slope != NULL) ? (brightX + (((double) i) - bleftY)/(*r_slope)) : brightX);
    r_bound = ((cur_rightX >= width) ? (width-1) : floor_441(cur_rightX));

    cur_leftZ = ((topZ==bleftZ) ? bleftZ : bleftZ + ((topZ - bleftZ)/(topY - bleftY)) * ((double) i - brightY));
    cur_leftRed = ((topRed == bleft_red) ? bleft_red : bleft_red + ((topRed - bleft_red)/(topY - bleftY)) * ((double) i - brightY));
    cur_leftGreen = ((topGreen == bleft_green) ? bleft_green : bleft_green + ((topGreen - bleft_green)/(topY - bleftY)) * ((double) i - brightY));
    cur_leftBlue = ((topBlue == bleft_blue) ? bleft_blue : bleft_blue + ((topBlue - bleft_blue)/(topY - bleftY)) * ((double) i - brightY));

    cur_rightZ = ((topZ == brightZ) ? brightZ : brightZ + ((topZ - brightZ)/(topY - brightY)) * ((double) i - brightY));
    cur_rightRed = ((topRed == bright_red) ? bright_red : bright_red + ((topRed - bright_red)/(topY - brightY)) * ((double) i - brightY));
    cur_rightGreen = ((topGreen == bright_green) ? bright_green : bright_green + ((topGreen - bright_green)/(topY-brightY))*((double)i - brightY));
    cur_rightBlue = ((topBlue == bright_blue) ? bright_blue : bright_blue + ((topBlue - bright_blue)/(topY - brightY))*((double) i - brightY));


    for(int j = l_bound; j <= r_bound; j++){
      cur_Z     = ((cur_rightZ - cur_leftZ)/(cur_rightX - cur_leftX))*((double) j - cur_leftX) + cur_leftZ;
      cur_red   = ((cur_rightRed - cur_leftRed)/(cur_rightX - cur_leftX))*((double) j - cur_leftX) + cur_leftRed;
      cur_green = ((cur_rightGreen - cur_leftGreen)/(cur_rightX - cur_leftX))*((double) j - cur_leftX) + cur_leftGreen;
      cur_blue  = ((cur_rightBlue - cur_leftBlue)/(cur_rightX - cur_leftX))*((double) j - cur_leftX) + cur_leftBlue;

      int pixel = width*i + j;
      int index = 3*pixel;

      if((cur_Z >= zVals[pixel]) && (cur_Z <= 0.0) && (cur_Z >= -1.0)){
        int r;
        int g;
        int b;
        r = ceil_441(255*cur_red);
        g = ceil_441(255*cur_green);
        b = ceil_441(255*cur_blue);

        buffer[index]     = r;
        buffer[index + 1] = g;
        buffer[index + 2] = b;

        zVals[pixel] = cur_Z;
      }
    }
  }
}

void RasterizeGoingDownTriangle(Triangle triangle, unsigned char *buffer, int width, int height, double* zVals){
  double bleftX, bleftY, bleftZ, brightX, brightY, brightZ, topX, topY, topZ;
  double bleft_red, bleft_green, bleft_blue, bright_red, bright_green, bright_blue, topRed, topGreen, topBlue;
  double cur_leftRed, cur_leftGreen, cur_leftBlue, cur_rightRed, cur_rightGreen, cur_rightBlue;
  double cur_red, cur_green, cur_blue;

  if(triangle.Y[0] == triangle.Y[1]){
    brightY = triangle.Y[0];
    bleftY  = triangle.Y[0];
    if(triangle.X[0] < triangle.X[1]){
      bleftX     = triangle.X[0];
      bleftZ     = triangle.Z[0];
      bleft_red   = triangle.color[0][0];
      bleft_green = triangle.color[0][1];
      bleft_blue  = triangle.color[0][2];

      brightX     = triangle.X[1];
      brightZ     = triangle.Z[1];
      bright_red   = triangle.color[1][0];
      bright_green = triangle.color[1][1];
      bright_blue  = triangle.color[1][2];
    }
    else{
      bleftX     = triangle.X[1];
      bleftZ     = triangle.Z[1];
      bleft_red   = triangle.color[1][0];
      bleft_green = triangle.color[1][1];
      bleft_blue  = triangle.color[1][2];

      brightX     = triangle.X[0];
      brightZ     = triangle.Z[0];
      bright_red   = triangle.color[0][0];
      bright_green = triangle.color[0][1];
      bright_blue  = triangle.color[0][2];
    }
    topX     = triangle.X[2];
    topY     = triangle.Y[2];
    topZ     = triangle.Z[2];
    topRed   = triangle.color[2][0];
    topGreen = triangle.color[2][1];
    topBlue  = triangle.color[2][2];
  }
  else if(triangle.Y[0] == triangle.Y[2]){
    brightY = triangle.Y[0];
    bleftY  = triangle.Y[0];
    if(triangle.X[0] < triangle.X[2]){
      bleftX     = triangle.X[0];
      bleftZ     = triangle.Z[0];
      bleft_red   = triangle.color[0][0];
      bleft_green = triangle.color[0][1];
      bleft_blue  = triangle.color[0][2];

      brightX     = triangle.X[2];
      brightZ     = triangle.Z[2];
      bright_red   = triangle.color[2][0];
      bright_green = triangle.color[2][1];
      bright_blue  = triangle.color[2][2];
    }
    else{
      bleftX     = triangle.X[2];
      bleftZ     = triangle.Z[2];
      bleft_red   = triangle.color[2][0];
      bleft_green = triangle.color[2][1];
      bleft_blue  = triangle.color[2][2];

      brightX     = triangle.X[0];
      brightZ     = triangle.Z[0];
      bright_red   = triangle.color[0][0];
      bright_green = triangle.color[0][1];
      bright_blue  = triangle.color[0][2];
    }
    topX = triangle.X[1];
    topY = triangle.Y[1];
    topZ = triangle.Z[1];
    topRed   = triangle.color[1][0];
    topGreen = triangle.color[1][1];
    topBlue  = triangle.color[1][2];
  }
  else{
    brightY = triangle.Y[1];
    bleftY  = triangle.Y[1];
    if(triangle.X[1] < triangle.X[2]){
      bleftX     = triangle.X[1];
      bleftZ     = triangle.Z[1];
      bleft_red   = triangle.color[1][0];
      bleft_green = triangle.color[1][1];
      bleft_blue  = triangle.color[1][2];

      brightX     = triangle.X[2];
      brightZ     = triangle.Z[2];
      bright_red   = triangle.color[2][0];
      bright_green = triangle.color[2][1];
      bright_blue  = triangle.color[2][2];
    }
    else{
      bleftX     = triangle.X[2];
      bleftZ     = triangle.Z[2];
      bleft_red   = triangle.color[2][0];
      bleft_green = triangle.color[2][1];
      bleft_blue  = triangle.color[2][2];

      brightX     = triangle.X[1];
      brightZ     = triangle.Z[1];
      bright_red   = triangle.color[1][0];
      bright_green = triangle.color[1][1];
      bright_blue  = triangle.color[1][2];
    }
    topX     = triangle.X[0];
    topY     = triangle.Y[0];
    topZ     = triangle.Z[0];
    topRed   = triangle.color[0][0];
    topGreen = triangle.color[0][1];
    topBlue  = triangle.color[0][2];
  }

  int ymin = ((topY < 0) ? 0 : ceil_441(topY));
  int ymax = ((bleftY >= height) ? (height - 1) : floor_441(bleftY));


  double* l_slope;
  double* r_slope;

  if(topX == bleftX){
    l_slope = NULL;
  }
  else{
    double val1 = (topY - bleftY)/(topX - bleftX);
    l_slope = &val1;
  }
  if(topX == brightX){
    r_slope = NULL;
  }
  else{
    double val2 = (brightY - topY)/(brightX - topX);
    r_slope = &val2;
  }

  for(int i = ymin; i <= ymax; i++){
    int r_bound, l_bound;
    double cur_leftX, cur_rightX, cur_leftZ, cur_rightZ, cur_Z;


    if(l_slope != NULL){
      double val1 = (((double) i) - topY)/(*l_slope);
      cur_leftX = topX + val1;
    }
    else{
      cur_leftX = bleftX;
    }

    l_bound = ((cur_leftX < 0) ? 0 : ceil_441(cur_leftX));

    if(r_slope != NULL){
      double val2 = (((double) i) - topY)/(*r_slope);
      cur_rightX = topX + val2;
    }
    else{
      cur_rightX = brightX;
    }

    r_bound = ((cur_rightX >= width) ? (width-1) : floor_441(cur_rightX));
    cur_leftZ = ((topZ == bleftZ) ? bleftZ : bleftZ + ((topZ - bleftZ)/(topY - bleftY)) * ((double) i - brightY));
    cur_leftRed = ((topRed == bleft_red) ? bleft_red : bleft_red + ((topRed - bleft_red) / (topY - bleftY)) * ((double) i - brightY));
    cur_leftGreen = ((topGreen == bleft_green) ? bleft_green : bleft_green + ((topGreen - bleft_green)/(topY - bleftY)) *((double) i - brightY));
    cur_leftBlue = ((topBlue == bleft_blue) ? bleft_blue : bleft_blue + ((topBlue - bleft_blue)/(topY - bleftY)) * ((double) i - brightY));

    cur_rightZ =((topZ == brightZ) ? brightZ : brightZ + ((topZ - brightZ)/(topY - brightY)) * ((double) i - brightY));
    cur_rightRed = ((topRed == bright_red) ? bright_red : bright_red + ((topRed - bright_red) / (topY - brightY)) * ((double) i - brightY));
    cur_rightGreen = ((topGreen == bright_green) ? bright_green : bright_green + ((topGreen - bright_green) / (topY - brightY)) * ((double) i - brightY));
    cur_rightBlue = ((topBlue == bright_blue) ? bright_blue : bright_blue + ((topBlue - bright_blue) / (topY - brightY)) * ((double) i - brightY));


    for(int j = l_bound; j <= r_bound; j++){
      cur_Z     = ((cur_rightZ - cur_leftZ)/(cur_rightX - cur_leftX))*(j - cur_leftX) + cur_leftZ;
      cur_red   = ((cur_rightRed - cur_leftRed)/(cur_rightX - cur_leftX))*(j - cur_leftX) + cur_leftRed;
      cur_green = ((cur_rightGreen - cur_leftGreen)/(cur_rightX - cur_leftX))*(j - cur_leftX) + cur_leftGreen;
      cur_blue  = ((cur_rightBlue - cur_leftBlue)/(cur_rightX - cur_leftX))*(j - cur_leftX) + cur_leftBlue;

      int pixel = width*i + j;

      int index = 3*pixel;

      if((cur_Z >= zVals[pixel]) && (cur_Z <= 0.0) && (cur_Z >= -1.0)){
        int r;
        int g;
        int b;
        r = ceil_441(255*cur_red);
        g = ceil_441(255*cur_green);
        b = ceil_441(255*cur_blue);

        buffer[index]     = r;
        buffer[index + 1] = g;
        buffer[index + 2] = b;

        zVals[pixel] = cur_Z;
      }
    }
  }

}

void RenderTriangles(Triangle triangle, Matrix m, unsigned char* buffer, int width, int height, double* zVals)
{
    double minX, midX, maxX;
    double minY, midY, maxY;
    double minZ, midZ, maxZ;
    double minRed, midRed, maxRed;
    double minGreen, midGreen, maxGreen;
    double minBlue, midBlue, maxBlue;

    if(triangle.Y[0] == triangle.Y[1]){
        if(triangle.Y[2] > triangle.Y[0]){
            RasterizeGoingUpTriangle(triangle, buffer, width, height, zVals);
        }
        else{
            RasterizeGoingDownTriangle(triangle, buffer, width, height, zVals);
        }
    }
    else if(triangle.Y[0] == triangle.Y[2])
    {
        if(triangle.Y[1] > triangle.Y[0]){
            RasterizeGoingUpTriangle(triangle, buffer, width, height, zVals);
        }
        else
        {
            RasterizeGoingDownTriangle(triangle, buffer, width, height, zVals);
        }
    }
    else if(triangle.Y[1] == triangle.Y[2])
    {
        if(triangle.Y[0] > triangle.Y[1]){
            RasterizeGoingUpTriangle(triangle, buffer, width, height, zVals);
        }
        else{
            RasterizeGoingDownTriangle(triangle, buffer, width, height, zVals);
        }
    }

    else{
        minY = triangle.Y[0];
        maxY = triangle.Y[0];
        midY = triangle.Y[0];
        minX = triangle.X[0];
        maxX = triangle.X[0];
        midX = triangle.X[0];
        minZ = triangle.Z[0];
        maxZ = triangle.Z[0];
        midZ = triangle.Z[0];
        maxRed = triangle.color[0][0];
        maxGreen = triangle.color[0][1];
        maxBlue = triangle.color[0][2];
        minRed = triangle.color[0][0];
        minGreen = triangle.color[0][1];
        minBlue = triangle.color[0][2];
        midRed = triangle.color[0][0];
        midGreen = triangle.color[0][1];
        midBlue = triangle.color[0][2];

        for(int k = 1; k<3; k++){
            if(triangle.Y[k] > maxY){
                maxY = triangle.Y[k];
                maxX = triangle.X[k];
                maxZ = triangle.Z[k];
                maxRed = triangle.color[k][0];
                maxGreen = triangle.color[k][1];
                maxBlue = triangle.color[k][2];
            }
            if(triangle.Y[k] < minY){
                minY = triangle.Y[k];
                minX = triangle.X[k];
                minZ = triangle.Z[k];
                minRed = triangle.color[k][0];
                minGreen = triangle.color[k][1];
                minBlue = triangle.color[k][2];
            }
        }

        for(int k = 0; k<3; k++){
            if((triangle.Y[k] < maxY) && (triangle.Y[k] > minY)){
                midY = triangle.Y[k];
                midX = triangle.X[k];
                midZ = triangle.Z[k];
                midRed = triangle.color[k][0];
                midGreen = triangle.color[k][1];
                midBlue = triangle.color[k][2];
            }
        }

        double newX;
        double newZ;
        double newRed;
        double newGreen;
        double newBlue;

        newX = minX + ((maxX - minX)/(maxY - minY))*(midY - minY);
        newZ = minZ + ((maxZ - minZ)/(maxY - minY))*(midY - minY);
        newRed = minRed + ((maxRed - minRed)/(maxY - minY))*(midY - minY);
        newGreen = minGreen + ((maxGreen - minGreen)/(maxY - minY))*(midY - minY);
        newBlue = minBlue + ((maxBlue - minBlue)/(maxY - minY))*(midY - minY);

        std::vector<Triangle> rv(2);

        Triangle triangle1 = rv[0];
        Triangle triangle2 = rv[1];

        triangle1.Y[0] = maxY;
        triangle1.X[0] = maxX;
        triangle1.Z[0] = maxZ;

        triangle1.Y[1] = midY;
        triangle1.X[1] = midX;
        triangle1.Z[1] = midZ;

        triangle1.Y[2] = midY;
        triangle1.X[2] = newX;
        triangle1.Z[2] = newZ;

        triangle1.color[0][0] = maxRed;
        triangle1.color[0][1] = maxGreen;
        triangle1.color[0][2] = maxBlue;
        triangle1.color[1][0] = midRed;
        triangle1.color[1][1] = midGreen;
        triangle1.color[1][2] = midBlue;
        triangle1.color[2][0] = newRed;
        triangle1.color[2][1] = newGreen;
        triangle1.color[2][2] = newBlue;

        triangle2.Y[0] = minY;
        triangle2.X[0] = minX;
        triangle2.Z[0] = minZ;

        triangle2.Y[1] = midY;
        triangle2.X[1] = midX;
        triangle2.Z[1] = midZ;

        triangle2.Y[2] = midY;
        triangle2.X[2] = newX;
        triangle2.Z[2] = newZ;

        triangle2.color[0][0] = minRed;
        triangle2.color[0][1] = minGreen;
        triangle2.color[0][2] = minBlue;
        triangle2.color[1][0] = midRed;
        triangle2.color[1][1] = midGreen;
        triangle2.color[1][2] = midBlue;
        triangle2.color[2][0] = newRed;
        triangle2.color[2][1] = newGreen;
        triangle2.color[2][2] = newBlue;


        RasterizeGoingUpTriangle(triangle1, buffer, width, height, zVals);

        RasterizeGoingDownTriangle(triangle2, buffer, width, height, zVals);
        }

    }

Triangle Triangle_To_DeviceSpace(Triangle t, Matrix m)
{
    Triangle newT;
    for (int i = 0; i < 3; i++)
    {
        double pointIn[4];
        pointIn[0] = t.X[i];
        pointIn[1] = t.Y[i];
        pointIn[2] = t.Z[i];
        pointIn[3] = 1;
        double pointOut[4];
        m.TransformPoint(pointIn, pointOut);
        newT.X[i] = pointOut[0] / pointOut[3];
        newT.Y[i] = pointOut[1] / pointOut[3];
        newT.Z[i] = pointOut[2] / pointOut[3];
    }
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            newT.color[i][j] = t.color[i][j];
        }
    }
    return newT;
}

std::vector<Triangle>
GetTriangles(void)
{
    vtkPolyDataReader *rdr = vtkPolyDataReader::New();
    rdr->SetFileName("proj1e_geometry.vtk");
    cerr << "Reading" << endl;
    rdr->Update();
    cerr << "Done reading" << endl;
    if (rdr->GetOutput()->GetNumberOfCells() == 0)
    {
        cerr << "Unable to open file!!" << endl;
        exit(EXIT_FAILURE);
    }
    vtkPolyData *pd = rdr->GetOutput();

    int numTris = pd->GetNumberOfCells();
    vtkPoints *pts = pd->GetPoints();
    vtkCellArray *cells = pd->GetPolys();
    vtkDoubleArray *var = (vtkDoubleArray *) pd->GetPointData()->GetArray("hardyglobal");
    double *color_ptr = var->GetPointer(0);
    //vtkFloatArray *var = (vtkFloatArray *) pd->GetPointData()->GetArray("hardyglobal");
    //float *color_ptr = var->GetPointer(0);
    vtkFloatArray *n = (vtkFloatArray *) pd->GetPointData()->GetNormals();
    float *normals = n->GetPointer(0);
    std::vector<Triangle> tris(numTris);
    vtkIdType npts;
    vtkIdType *ptIds;
    int idx;
    for (idx = 0, cells->InitTraversal() ; cells->GetNextCell(npts, ptIds) ; idx++)
    {
        if (npts != 3)
        {
            cerr << "Non-triangles!! ???" << endl;
            exit(EXIT_FAILURE);
        }
        double *pt = NULL;
        pt = pts->GetPoint(ptIds[0]);
        tris[idx].X[0] = pt[0];
        tris[idx].Y[0] = pt[1];
        tris[idx].Z[0] = pt[2];
#ifdef NORMALS
        tris[idx].normals[0][0] = normals[3*ptIds[0]+0];
        tris[idx].normals[0][1] = normals[3*ptIds[0]+1];
        tris[idx].normals[0][2] = normals[3*ptIds[0]+2];
#endif
        pt = pts->GetPoint(ptIds[1]);
        tris[idx].X[1] = pt[0];
        tris[idx].Y[1] = pt[1];
        tris[idx].Z[1] = pt[2];
#ifdef NORMALS
        tris[idx].normals[1][0] = normals[3*ptIds[1]+0];
        tris[idx].normals[1][1] = normals[3*ptIds[1]+1];
        tris[idx].normals[1][2] = normals[3*ptIds[1]+2];
#endif
        pt = pts->GetPoint(ptIds[2]);
        tris[idx].X[2] = pt[0];
        tris[idx].Y[2] = pt[1];
        tris[idx].Z[2] = pt[2];
#ifdef NORMALS
        tris[idx].normals[2][0] = normals[3*ptIds[2]+0];
        tris[idx].normals[2][1] = normals[3*ptIds[2]+1];
        tris[idx].normals[2][2] = normals[3*ptIds[2]+2];
#endif

        // 1->2 interpolate between light blue, dark blue
        // 2->2.5 interpolate between dark blue, cyan
        // 2.5->3 interpolate between cyan, green
        // 3->3.5 interpolate between green, yellow
        // 3.5->4 interpolate between yellow, orange
        // 4->5 interpolate between orange, brick
        // 5->6 interpolate between brick, salmon
        double mins[7] = { 1, 2, 2.5, 3, 3.5, 4, 5 };
        double maxs[7] = { 2, 2.5, 3, 3.5, 4, 5, 6 };
        unsigned char RGB[8][3] = { { 71, 71, 219 },
                                    { 0, 0, 91 },
                                    { 0, 255, 255 },
                                    { 0, 128, 0 },
                                    { 255, 255, 0 },
                                    { 255, 96, 0 },
                                    { 107, 0, 0 },
                                    { 224, 76, 76 }
                                  };
        for (int j = 0 ; j < 3 ; j++)
        {
            float val = color_ptr[ptIds[j]];
            int r;
            for (r = 0 ; r < 7 ; r++)
            {
                if (mins[r] <= val && val < maxs[r])
                    break;
            }
            if (r == 7)
            {
                cerr << "Could not interpolate color for " << val << endl;
                exit(EXIT_FAILURE);
            }
            double proportion = (val-mins[r]) / (maxs[r]-mins[r]);
            tris[idx].color[j][0] = (RGB[r][0]+proportion*(RGB[r+1][0]-RGB[r][0]))/255.0;
            tris[idx].color[j][1] = (RGB[r][1]+proportion*(RGB[r+1][1]-RGB[r][1]))/255.0;
            tris[idx].color[j][2] = (RGB[r][2]+proportion*(RGB[r+1][2]-RGB[r][2]))/255.0;
        }
    }

    return tris;

}

vtkImageData *
NewImage(int width, int height)
{
    vtkImageData *img = vtkImageData::New();
    img->SetDimensions(width, height, 1);
    img->AllocateScalars(VTK_UNSIGNED_CHAR, 3);

    return img;
}

void
WriteImage(vtkImageData *img, const char *filename)
{
   std::string full_filename = filename;
   full_filename += ".png";
   vtkPNGWriter *writer = vtkPNGWriter::New();
   writer->SetInputData(img);
   writer->SetFileName(full_filename.c_str());
   writer->Write();
   writer->Delete();
}

void SaveImage(vtkImageData *image, int count)
{
    std::string iName;
    std::ostringstream convert;
    if (count < 10)
    {
      convert << "frame00" << count;
    }
    else if ((count < 100) && (count > 10)){
      convert << "frame0" << count;
    }
    else{
      convert << "frame" << count;
    }
    iName = convert.str();
    const char * c = iName.c_str();
    WriteImage(image, c);
}




void
initializeBuffer(unsigned char* buffer, int npixels)
{
    for(int i = 0; i < npixels*3; i++)
    {
        buffer[i] = 0;
    }

}

int main()
{
  int width = 1000;
  int height = 1000;
  vtkImageData *image = NewImage(width, height);
  unsigned char *buffer =
    (unsigned char *) image->GetScalarPointer(0,0,0);

  int npixels = width*height;
  initializeBuffer(buffer, npixels);

  std::vector<Triangle> triangles = GetTriangles();
  double zVals[npixels];

  std::fill_n(zVals, npixels, -1.0);

  Screen screen;
  Camera camera;

    for (int i = 0; i < 1000; i+=250)
    {
        screen = InitializeScreen(buffer, width, height);
        camera = GetCamera(i, 1000);
        camera.CameraTransform();
        camera.ViewTransform();
        camera.DeviceTransform(screen);

        Matrix m = Matrix::ComposeMatrices(
                   Matrix::ComposeMatrices(camera._CameraTransform,
                                             camera._ViewTransform),
                                             camera._DeviceTransform);

        for (int j = 0; j < triangles.size(); j++)
        {
            Triangle tri = triangles[j];
            Triangle triangle = Triangle_To_DeviceSpace(tri, m);

            triangle.screen = screen;
            RenderTriangles(triangle, m, buffer, width, height, triangle.screen.zBuffer);
        }

        SaveImage(image, i);

    }
}
