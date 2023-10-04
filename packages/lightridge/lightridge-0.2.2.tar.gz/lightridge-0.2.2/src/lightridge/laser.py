import torch
import numpy as np
import torch.nn.functional as F	

class RingAperture(torch.nn.Module):

    """This function describes a (Frensel) diffraction pattern of a ring aperture
    
    Input Args: 
    radius: the radius of ring aperture
    distance: the distance between the aperture and next screen
    mesh_size: the number of points in a single pixel
    
    """

    def __init__(self, radius=3.6e-3, wavelength=5.32e-7, pixel_size=3.6e-5, size=100, distance=0.1, mesh_size=10, pad=1):
        
        super(RingAperture, self).__init__()
        self.radius = radius
        self.size = size * mesh_size
        self.distance = distance
        self.mesh_size = mesh_size
        self.pixel_size = pixel_size/self.mesh_size
        self.ll = self.pixel_size * self.size
        self.wl = wavelength                 
        self.fi = 1 / self.ll                 
        self.wn = 2 * 3.1415926 / self.wl
        self.pad = pad

        r = np.fromfunction(
            lambda x, y: np.square((x - (self.size + self.pad*2) // 2) * self.pixel_size) + np.square((y - (self.size + self.pad*2) // 2) * self.pixel_size), shape=(self.size + self.pad*2, self.size + self.pad*2), dtype=np.float64)

        ## define an aperture 

        aperture_mask = np.fromfunction(
            lambda x, y: np.sqrt(np.square((x - (self.size + self.pad*2) // 2) * self.pixel_size) + np.square((y - (self.size + self.pad*2) // 2) * self.pixel_size)) < self.radius, shape=(self.size + self.pad*2, self.size + self.pad*2), dtype=np.float64)

        aperture_mask = aperture_mask.astype(np.float64)    

        mask = torch.from_numpy(aperture_mask[self.pad:self.size + self.pad, self.pad:self.size + self.pad])
        mask = torch.unsqueeze(mask, dim=0)
        mask = torch.unsqueeze(mask, dim=0)
        layer = torch.nn.AvgPool2d(self.mesh_size)
        self.mask = layer(mask).squeeze() 

        h = np.exp(1.0j * self.wn * self.distance) * np.exp(1.0j * self.wn/2/distance * r)/(1.0j * self.wl * distance)
        h = torch.from_numpy(h)
        h = torch.fft.fftshift(h)
        self.h = torch.nn.Parameter(torch.fft.fft2(h.to(torch.complex64)), requires_grad=False)

    # def forward(self, waves):
    #     return waves * self.h
    def forward(self, waves):
        # waves (batch, 200, 200, 2)
        waves = torch.repeat_interleave(waves, self.mesh_size, dim=1)
        waves = torch.repeat_interleave(waves, self.mesh_size, dim=0)
        
        waves = torch.nn.functional.pad(waves, (self.pad,self.pad,self.pad,self.pad)) # pad to eliminate perodic effects 
        temp = torch.fft.ifft2(torch.fft.fft2(waves) * self.h) # prop
        temp = torch.nn.functional.pad(temp, (-self.pad,-self.pad,-self.pad,-self.pad)) # reverse pad for next prop (center crop)

        temp_real = torch.view_as_real(temp)[:,:,0]
        temp_imag = torch.view_as_real(temp)[:,:,1]
        temp_real = torch.unsqueeze(temp_real, dim=0)
        temp_real = torch.unsqueeze(temp_real, dim=0)
        temp_imag = torch.unsqueeze(temp_imag, dim=0)
        temp_imag = torch.unsqueeze(temp_imag, dim=0)

        layer = torch.nn.AvgPool2d(self.mesh_size)

        temp_real = layer(temp_real).squeeze()
        temp_imag = layer(temp_imag).squeeze()

        temp = torch.view_as_complex(torch.stack((temp_real, temp_imag), dim=-1))

        return temp

class RectAperture(torch.nn.Module):


    """This function describes a (Frensel) diffraction pattern of a rectangular aperture
    
    Input Args: 
    xdim, ydim: the x and y lateral dimensions of rectangular aperture
    distance: the distance between the aperture and next screen
    mesh_size: the number of points in a single pixel
    
    """

    def __init__(self, xdim=3.6e-3, ydim=3.6e-3, wavelength=5.32e-7, pixel_size=3.6e-5, size=100, distance=0.1, mesh_size=10, pad=1):
        
        super(RectAperture, self).__init__()
        self.xdim = xdim
        self.ydim = ydim
        self.size = size * mesh_size
        self.distance = distance
        self.mesh_size = mesh_size
        self.pixel_size = pixel_size/self.mesh_size
        self.ll = self.pixel_size * self.size
        self.wl = wavelength                 
        self.fi = 1 / self.ll                 
        self.wn = 2 * 3.1415926 / self.wl
        self.pad = pad

        r = np.fromfunction(
            lambda x, y: np.square((x - (self.size + self.pad*2) // 2) * self.pixel_size) + np.square((y - (self.size + self.pad*2) // 2) * self.pixel_size), shape=(self.size + self.pad*2, self.size + self.pad*2), dtype=np.float64)

        ## define an aperture 

        aperture_mask = np.zeros([self.size + self.pad*2, self.size + self.pad*2])
        x_index_num = int(self.xdim/self.pixel_size)
        y_index_num = int(self.ydim/self.pixel_size)
        test = aperture_mask[self.size//2 + self.pad - x_index_num//2: self.size//2 + self.pad + x_index_num//2, 
                      self.size//2 + self.pad - y_index_num//2: self.size//2 + self.pad + y_index_num//2]
        aperture_mask[self.size//2 + self.pad - x_index_num//2: self.size//2 + self.pad + x_index_num//2, 
                      self.size//2 + self.pad - y_index_num//2: self.size//2 + self.pad + y_index_num//2] = np.ones(test.shape)

        mask = torch.from_numpy(aperture_mask[self.pad:self.size + self.pad, self.pad:self.size + self.pad])
        mask = torch.unsqueeze(mask, dim=0)
        mask = torch.unsqueeze(mask, dim=0)
        layer = torch.nn.AvgPool2d(self.mesh_size)
        self.mask = layer(mask).squeeze() 
        ###

        h = np.exp(1.0j * self.wn * self.distance) * np.exp(1.0j * self.wn/2/distance * r)/(1.0j * self.wl * distance)
        h = torch.from_numpy(h)
        h = torch.fft.fftshift(h)
        self.h = torch.nn.Parameter(torch.fft.fft2(h.to(torch.complex64)), requires_grad=False)

    # def forward(self, waves):
    #     return waves * self.h
    def forward(self, waves):
        # waves (batch, 200, 200, 2)
        waves = torch.repeat_interleave(waves, self.mesh_size, dim=1)
        waves = torch.repeat_interleave(waves, self.mesh_size, dim=0)

        waves = torch.nn.functional.pad(waves, (self.pad,self.pad,self.pad,self.pad)) # pad to eliminate perodic effects 
        temp = torch.fft.ifft2(torch.fft.fft2(waves) * self.h) # prop
        temp = torch.nn.functional.pad(temp, (-self.pad,-self.pad,-self.pad,-self.pad)) # reverse pad for next prop (center crop)

        temp_real = torch.view_as_real(temp)[:,:,0]
        temp_imag = torch.view_as_real(temp)[:,:,1]
        temp_real = torch.unsqueeze(temp_real, dim=0)
        temp_real = torch.unsqueeze(temp_real, dim=0)
        temp_imag = torch.unsqueeze(temp_imag, dim=0)
        temp_imag = torch.unsqueeze(temp_imag, dim=0)

        layer = torch.nn.AvgPool2d(self.mesh_size)

        temp_real = layer(temp_real).squeeze()
        temp_imag = layer(temp_imag).squeeze()

        temp = torch.view_as_complex(torch.stack((temp_real, temp_imag), dim=-1))

        return temp

class GaussBeam(torch.nn.Module):

    '''
    This function describes the beam profile of incident light
    Args:
    profile_name: by default it is Gaussian
    '''

    def __init__(self, pixel_size=3.6e-5, size=100, waist=1e-3 ,pad=0):

        super(GaussBeam).__init__()
        self.pixel_size = pixel_size
        self.size = size
        self.pad = pad
        self.waist = waist

        r = np.fromfunction(lambda x, y: np.square((x - (self.size + self.pad*2) // 2) * self.pixel_size) + np.square((y - (self.size + self.pad*2) // 2) * self.pixel_size), shape=(self.size + self.pad*2, self.size + self.pad*2), dtype=np.float64)

        r = torch.from_numpy(r)
        
        self.r = r

    def forward(self, waves):

        output = waves * torch.exp(-self.r/self.waist/self.waist)
        
        return output
