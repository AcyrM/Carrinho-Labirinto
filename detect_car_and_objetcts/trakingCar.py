
# Recebe o shape do carro
car_contours = tracking_car_detect_obj(frame.copy())
# Centro da coordenada x e y = centro do carrinho -> tupla
car_center_pixel = (int(obj[0]+((obj[0]+obj[2])/2)), int(obj[1]+((obj[1]+obj[3])/2)))
# caminho a ser seguido
path_segment = 0

# Verifica se o pixel central do carrinho é igual ao proximo pixel do caminho
start = car_center_pixel
for p in range(len(path_size))
    if car_center_pixel[0] is not p[0]:
        if p[0] < car_center_pixel[0]:
            # andar para tras
        else:
            # andar para frente
    if car_center_pixel[1] is not p[1]:
        if p[1] < car_center_pixel[1]:
            # andar para cima
        else:
            # andar para baixo
