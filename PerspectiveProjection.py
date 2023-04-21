import pygame
from math import cos,sin,tan,radians
import numpy as np

class GraphicGeneration:
    def __init__(self,setup=False):
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.WIDTH, self.HEIGHT = 1200, 800
        
        pygame.display.set_caption("Perspective Projection")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        self.scale_x = 100
        self.scale_y = 100
        self.scale_z = 100

        self.circle_pos = [self.WIDTH/2, self.HEIGHT/2]

        self.anglex = 0
        self.angley = 0
        self.anglez = 0

        self.camera_angle_x=0
        self.camera_angle_y=0
        self.camera_angle_z=0

        self.move_x=0
        self.move_y=0
        self.move_z=0

        self.objects=[]
        self.createObjects()
        self.animation=False
        self.perspectiveProjection=False
        
        self.factor=0.1


        if setup:
            self.setup()
        else:
            f = 1 / tan(radians(np.radians(75) / 2))
            self.perspective_matrix = np.array([
            [f / 1, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (100.0 + 0.25) / (0.25 - 100.0), 2 * 100.0 * 0.25 / (0.25 - 100.0)],
            [0, 0, -1, 0]
        ])

        pass

    def setup(self):

        fov=int(input("Enter Field Of View : "))
        fov=radians(fov)

        aspect_ratio=self.WIDTH/self.HEIGHT  #float(input("Enter the aspect ratio of the screen"))

        near_clip=float(input("Enter how far is the screen from the user(in m) : "))
        far_clip=float(input("Enter until how far the object should render(in m) : "))

        f = 1 / tan(radians(fov / 2))
        self.perspective_matrix = np.array([
            [f / aspect_ratio, 0, 0, 0],
            [0, f, 0, 0],
            [0, 0, (far_clip + near_clip) / (near_clip - far_clip), 2 * far_clip * near_clip / (near_clip - far_clip)],
            [0, 0, -1, 0]
        ])

    def createObjects(self):
        if len(self.objects)==0:
            self.objects.append([
            np.array([0, -1, -1]),
            np.array([1, -1, -1]),
            np.array([1,  1, -1]),
            np.array([0, 1, -1]),
            np.array([0, -1, -2]),
            np.array([1, -1, -2]),
            np.array([1, 1, -2]),
            np.array([0, 1, -2])])

        elif len(self.objects)==1:
            self.objects.append([
            np.array([-2, -1, -3]),
            np.array([-1, -1, -3]),
            np.array([-1, 1, -3]),
            np.array([-2, 1, -3]),
            np.array([-2, -1, -4]),
            np.array([-1, -1, -4]),
            np.array([-1, 1, -4]),
            np.array([-2, 1, -4])])
        else:
            print("Maximum Objects Limit Reached")

    
    def connect_points(self,i, j, points):
        pygame.draw.line(
            self.screen, self.BLACK, (points[i][0], points[i][1]), (points[j][0], points[j][1]))
        

    def perspective_projection(self,points):
        points = np.hstack((points, np.ones((len(points), 1))))
        projected_points = np.dot(points,self.perspective_matrix)
        normalized_points = projected_points[:, :-1] / projected_points[:, -1].reshape((-1, 1))
        return normalized_points.tolist()

    def scaling(self,points):
        scaling_matrix=np.array([
            [self.scale_x,0,0,],
            [0,self.scale_y,0,],
            [0,0,self.scale_z,],
            
        ])
        return [np.dot(scaling_matrix,i) for i in points]
       


    def projection(self,points):
        projection_matrix = np.array([
            np.array([1, 0, 0]),
            np.array([0, 1, 0]),
            np.array([0,0,0]) ])
        
        return [np.dot(projection_matrix,i) for i in points]


    def translation(self,points):
        translation_matrix=np.array([
            [1,0,0,self.move_x],
            [0,1,0,self.move_y],
            [0,0,1,self.move_z],
            [0,0,0,1],
        ])
        
        points = np.hstack((points, np.ones((len(points), 1))))
        translated_points = np.dot(translation_matrix, points.T).T[:, :-1]
        return translated_points

    def rotate_along_axis(self,points):
        center = np.mean(points, axis=0)
        points=[p - center for p in points]
        
        rotation_x = np.array([
            [1, 0, 0],
            [0, cos(self.anglex), -sin(self.anglex)],
            [0, sin(self.anglex), cos(self.anglex)],
        ])

        rotation_y = np.array([
            [cos(self.angley), 0, sin(self.angley)],
            [0, 1, 0],
            [-sin(self.angley), 0, cos(self.angley)],
        ])

        rotation_z = np.array([
            [cos(self.anglez), -sin(self.anglez), 0],
            [sin(self.anglez), cos(self.anglez), 0],
            [0, 0, 1],
        ])

        rotation_matrix = np.dot(np.dot(rotation_x, rotation_y), rotation_z)
        return [center+np.dot(rotation_matrix, i) for i in points]
    

    def rotate_around_camera(self,points):
        rotation_x = np.array([
            [1, 0, 0],
            [0, cos(self.camera_angle_x), -sin(self.camera_angle_x)],
            [0, sin(self.camera_angle_x), cos(self.camera_angle_x)],
        ])

        rotation_y = np.array([
            [cos(self.camera_angle_y), 0, sin(self.camera_angle_y)],
            [0, 1, 0],
            [-sin(self.camera_angle_y), 0, cos(self.camera_angle_y)],
        ])

        rotation_z = np.array([
            [cos(self.camera_angle_z), -sin(self.camera_angle_z), 0],
            [sin(self.camera_angle_z), cos(self.camera_angle_z), 0],
            [0, 0, 1],
        ])

        rotation_matrix = np.dot(np.dot(rotation_x, rotation_y), rotation_z)
        return [np.dot(rotation_matrix, i) for i in points]


    def join_points(self,projected_points):
        for p in range(4):
                self.connect_points(p, (p+1) % 4, projected_points)
                self.connect_points(p+4, ((p+1) % 4) + 4, projected_points)
                self.connect_points(p, (p+4), projected_points)


    def performMatrixOperation(self):
        transformedObjects=[]
        for points in self.objects:
            points=self.rotate_along_axis(points)
            points=self.rotate_around_camera(points)
            points=self.scaling(points)
            points=self.translation(points)
            if self.perspectiveProjection:
                points =self.perspective_projection(points)
            else:
                pass
            transformedObjects.append(points)

        
        for points in transformedObjects:
            projected_points=[]
            for projected2d in points:
                x = int(projected2d[0]) + self.circle_pos[0]
                y = int(projected2d[1]) + self.circle_pos[1]
                projected_points.append([x, y])
                pygame.draw.circle(self.screen, self.RED, (x, y), 5)
            self.join_points(projected_points)

        
        
    def animate(self):
        if self.animation:
            self.anglex+=0.001
            self.angley+=-0.002
            self.anglez+=0.001
        # elif self.animation==2:
        #     if self.move_x+self.factor>=1200 or self.move_x+self.factor<=800:
        #         self.factor*=-1
        #     self.move_x+=self.factor
            
        # elif self.animation==3:
        #     if self.scale_x+self.factor<=0.5 or self.scale_x+self.factor>=5:
        #         self.factor=-1*self.factor
        #     self.scale_x+=self.factor
        #     pass

        

    def main(self):
        clock = pygame.time.Clock()


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        exit()
                        #Arrow keys rotation around camera
                    elif event.key == pygame.K_UP:
                        self.camera_angle_z += 0.1
                    elif event.key == pygame.K_DOWN:
                        self.camera_angle_z -= 0.1
                    elif event.key == pygame.K_LEFT:
                        self.camera_angle_y += 0.1
                    elif event.key == pygame.K_RIGHT:
                        self.camera_angle_y -= 0.1
                    elif event.key == pygame.K_RCTRL:
                        self.camera_angle_x += 0.1
                    elif event.key == pygame.K_KP0:
                        self.camera_angle_x -= 0.1

                    #numpad keys for object rotation along its axis
                    elif event.key == pygame.K_KP8:
                        self.anglez += 0.1
                    elif event.key == pygame.K_KP2:
                        self.anglez -= 0.1
                    elif event.key == pygame.K_KP4:
                        self.angley += 0.1
                    elif event.key == pygame.K_KP6:
                        self.angley -= 0.1
                    elif event.key == pygame.K_KP7:
                        self.anglex += 0.1
                    elif event.key == pygame.K_KP9:
                        self.anglex -= 0.1

                    #WASDQE for translation of object

                    elif event.key == pygame.K_w:
                        self.move_z += 1
                    elif event.key == pygame.K_s:
                        self.move_z -= 1
                    elif event.key == pygame.K_a:
                        self.move_y += 1
                    elif event.key == pygame.K_d:
                        self.move_y -= 1
                    elif event.key == pygame.K_q:
                        self.move_x += 1
                    elif event.key == pygame.K_e:
                        self.move_x -= 1

                    #ZX for scaling of object

                    elif event.key == pygame.K_i:
                        self.scale_z += 1
                    elif event.key == pygame.K_k:
                        self.scale_z -= 1
                    elif event.key == pygame.K_j:
                        self.scale_y += 1
                    elif event.key == pygame.K_l:
                        self.scale_y -= 1
                    elif event.key == pygame.K_u:
                        self.scale_x += 1
                    elif event.key == pygame.K_o:
                        self.scale_x -= 1


                    # Backslash toggling between projection and perspective

                    elif event.key == pygame.K_KP_DIVIDE:
                        self.perspectiveProjection=not self.perspectiveProjection

                    # - to start animation

                    elif event.key == pygame.K_KP_MINUS:
                        self.animation=not self.animation
                        # if self.animation==4:
                        #     self.animation=0

                    # + to add object 
                    elif event.key == pygame.K_KP_MULTIPLY:
                        self.createObjects()

            self.screen.fill(self.WHITE)
            if self.animation:
                self.animate()
            self.performMatrixOperation()
            
        
            pygame.display.update()




if __name__=='__main__':
    GraphicGeneration().main()
