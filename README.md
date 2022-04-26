# UC - Instrumentação e Aquisição de Dados
### Sistema de Rega, com 20 programas e 12 canais de rega

## To-Do
- [X] Dar o tempo ao Arduino
- [X] Confirmar leitura do tempo
- [X] Estrutura com os programas
- [X] Ras.PI - Editar os programas com botões
- [X] Ler os programas e mudar as coisas
- [X] Enviar os programas para o Arduino
- [ ] Fazer funcionar o circuito
- [X] Experimentar os sensores (verificar valores)
- [ ] Avisar se mudar de prog sem guardar

## Sugestões
- [ ] Incompatibilidade entre programas

## Informações
<table>
	<caption>Valores vistos na net</caption>
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

<table>
	<caption>Valores experimentais</caption>
	<tr>
		<th>Sensor in</th>
		<th>3.3 V</th>
		<th>5 V</th>
  	</tr>
  	<tr>
    		<td>Air</td>
    		<td>407</td>
    		<td>757</td>
  	</tr>
  	<tr>
		<td>Dry soil</td>
		<td>347</td>
		<td>740</td>
  	</tr>
  	<tr>
		<td>Semi-humid soil</td>
		<td>307</td>
		<td>712</td>
  	</tr>
  	<tr>
		<td>Humid soil</td>
		<td>262</td>
		<td>546</td>
  	</tr>
  	<tr>
		<td>Water</td>
		<td>253</td>
		<td>523</td>
  	</tr>
</table>


Digitos nas spinboxes: https://stackoverflow.com/questions/19172262/pyqt4-qspinbox-value-format
