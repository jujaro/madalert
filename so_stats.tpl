<head>
</head>
<body>
<h2>Last Day growth</h2>
<table border="1" cellpadding="0" cellspacing="0" style="width: 500px;">
	<thead>
		<tr>
			<th scope="col">
				No</th>
			<th scope="col">
				Technology</th>
			<th scope="col">
				Relative Growth</th>
			<th scope="col">
				Day Questions</th>
			<th scope="col">
				Week Questions</th>
			<th scope="col">
				Month Questions</th>
			<th scope="col">
				All Questions</th>
		</tr>
	</thead>
	<tbody>
% for i,tag in enumerate(top_day_growth):
		<tr>
			<td style = "text-align:right;">
				{{i+1}}</td>
			<td style = "text-align:right;">
				{{tag.tag_name}}</td>
			<td style = "text-align:right;">
				{{tag.day_growth()}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_day}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_week}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_month}}</td>
			<td style = "text-align:right;">
				{{tag.count}}</td>
		</tr>
% end
</table>

<h2>Last Week growth</h2>
<table border="1" cellpadding="0" cellspacing="0" style="width: 500px;">
	<thead>
		<tr>
			<th scope="col">
				No</th>
			<th scope="col">
				Technology</th>
			<th scope="col">
				Relative Growth</th>
			<th scope="col">
				Day Questions</th>
			<th scope="col">
				Week Questions</th>
			<th scope="col">
				Month Questions</th>
			<th scope="col">
				All Questions</th>
		</tr>
	</thead>
	<tbody>
% for i,tag in enumerate(top_week_growth):
		<tr>
			<td style = "text-align:right;">
				{{i+1}}</td>
			<td style = "text-align:right;">
				{{tag.tag_name}}</td>
			<td style = "text-align:right;">
				{{tag.week_growth()}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_day}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_week}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_month}}</td>
			<td style = "text-align:right;">
				{{tag.count}}</td>
		</tr>
% end
</table>

<h2>Last Month growth</h2>
<table border="1" cellpadding="0" cellspacing="0" style="width: 500px;">
	<thead>
		<tr>
			<th scope="col">
				No</th>
			<th scope="col">
				Technology</th>
			<th scope="col">
				Relative Growth</th>
			<th scope="col">
				Day Questions</th>
			<th scope="col">
				Week Questions</th>
			<th scope="col">
				Month Questions</th>
			<th scope="col">
				All Questions</th>
		</tr>
	</thead>
	<tbody>
% for i,tag in enumerate(top_month_growth):
		<tr>
			<td style = "text-align:right;">
				{{i+1}}</td>
			<td style = "text-align:right;">
				{{tag.tag_name}}</td>
			<td style = "text-align:right;">
				{{tag.month_growth()}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_day}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_week}}</td>
			<td style = "text-align:right;">
				{{tag.q_of_month}}</td>
			<td style = "text-align:right;">
				{{tag.count}}</td>
		</tr>
% end
</table>


</body>
