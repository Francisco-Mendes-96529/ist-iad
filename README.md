# UC - Instrumentação e Aquisição de Dados

## To-Do
- [ ] Dar o tempo ao Arduino
- [ ] Experimentar:
```
k=0
while ser.inWaiting() <= 0:
	time.sleep(0.01)
	k++
	if k==10:
		break
	
if ser.inWaiting() > 0:
	line = ser.readline().decode('utf-8').rstrip()  # Ler e traduz o que foi enviado pelo Arduino
	print(line)
else:
	print("buffer invalido")
```

## Sugestões
- [ ] Classe com os programas
- [ ] Ras.PI - Editar os programas com botões

## Informações
<table>
	<tr>
		<th>Sensor in</th>
		<th>3.3 V</th>
		<th>5 V</th>
  	</tr>
  	<tr>
    	<td>Dry soil</td>
    	<td>0</td>
    	<td>300</td>
  	</tr>
  	<tr>
		<td>Humid soil</td>
		<td>300</td>
		<td>700</td>
  	</tr>
  	<tr>
		<td>Water</td>
		<td>700</td>
		<td>950</td>
  	</tr>
</table>
