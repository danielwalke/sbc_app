<template>
	<div class="custom-height flex justify-center p-4 overflow-y-auto">
		<div class=" w-4/5">
			<div class="impressum">
				<h2>Impressum (Legal Disclosure)</h2>
				<p>
					<strong>Daniel Walke / Otto-von-Guericke University</strong><br>
					Universitätspl. 2<br/>
					39106 Magdeburg<br/>
					Germany<br/>
				</p>
				<p>
					<strong>Kontakt</strong><br>
					E-Mail: <a href="mailto:[your email address]">daniel.walke@ovgu.de</a><br>
				</p>
			</div>

			<div class="disclaimer">
				<h2>Disclaimer for Predictions</h2>
				<p>The predictions provided on this website are for informational purposes only and do not constitute professional advice. We strive to provide accurate and up-to-date information, but we cannot guarantee that the predictions are correct.</p>
				<p><strong>It is your sole responsibility to rely on the accuracy of the predictions.</strong> We assume no liability for any loss or damage suffered by you as a result of using the predictions provided on this website.</p>
				<h3>Important Notes</h3>
				<ul>
					<li>The predictions are based on data and algorithms that may be flawed.</li>
					<li>Unforeseen events can affect the accuracy of the predictions.</li>
					<li>You should use the predictions in conjunction with other information and your own judgment.</li>
				</ul>
			</div>

			<div class="disclaimer">
				<h2>Contributors</h2>
				<ul class="list-disc pl-5">
					<li>
						Daniel Walke
					</li>
					<li>
						Daniel Steinbach
					</li>
					<li>
						Thorsten Kaiser
					</li>
					<li>
						David Broneske
					</li>
					<li>
						Robert Heyer
					</li>
				</ul>
			</div>

			<div class="disclaimer">
				Current version: v.05
			</div>
		</div>
	</div>

</template>

<script setup lang="js">
</script>

<style scoped>
h2 {
	font-size: 1.5rem;
	margin-bottom: 1rem;
}
p {
	margin-bottom: 0.5rem;
}
.impressum, .disclaimer {
	border: 1px solid #ddd;
	padding: 1rem;
	margin-bottom: 2rem;
}
.impressum h3, .disclaimer h3 {
	font-size: 1.2rem;
	margin-top: 0;
}
.disclaimer a {
	text-decoration: none;
	color: #000;
}
div{
	@apply rounded-md p-2 leading-8
}
</style>
