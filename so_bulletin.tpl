<head>
</head>
<body>
<h2>SO Bulletin</h2>
<table border="1" cellpadding="0" cellspacing="0" style="width: 500px;">
	<thead>
		<tr>
			<th scope="col">
				Title</th>
			<th scope="col">
				Score</th>
			<th scope="col">
				Answers</th>
			<th scope="col">
				Link</th>
		</tr>
	</thead>
	<tbody>
% for i,question in enumerate(questions):
		<tr>
			<td style = "text-align:right;">
				{{question['title']}}</td>
			<td style = "text-align:right;">
				{{question['score']}}</td>
			<td style = "text-align:right;">
				{{question['answer_count']}}</td>
			<td style = "text-align:right;">
				<a href = "{{question['link']}}">link</a></td>
		</tr>
% end
</table>


</body>
