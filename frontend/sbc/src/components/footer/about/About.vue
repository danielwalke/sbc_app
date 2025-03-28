<template>
	<div class="custom-height w-full flex justify-center p-4 overflow-y-auto">
		<div class="w-full lg:w-4/5">
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

      <div class="container-fluid container-xxxl mt-2 flex-grow-1 py-2 d-flex flex-column">
        <h2>Exclusion of liability (disclaimer)</h2>
        <h3>Liability for content</h3>
        <p> As a service provider, we are responsible for our own content on these pages in accordance with §7 para.1 TMG (Deutsches Telemediengesetz) and general laws. According to §8 to 10 TMG, however, we as a service provider are not obliged to monitor transmitted or stored third-party information or to investigate circumstances that indicate illegal activity. Obligations to remove or block the use of information in accordance with general legislation remain unaffected by this. However, liability in this respect is only possible from the time of knowledge of a specific infringement. As soon as we become aware of such infringements, we will remove this content immediately. </p>
        <h3>Liability for links</h3>
        <p> Our website contains links to external third-party websites over whose content we have no influence. Therefore, we cannot accept any liability for this third-party content. The respective provider or operator of the pages is always responsible for the content of the linked pages. The linked pages were checked for possible legal violations at the time of linking. Illegal content was not recognizable at the time of linking. However, permanent monitoring of the content of the linked pages is not reasonable without concrete evidence of an infringement. If we become aware of any legal infringements, we will remove such links immediately. </p>
        <h2>Copyright</h2>
        <p> The content and works created by the site operators on these pages are subject to German copyright law. Duplication, processing, distribution and any form of commercialization of such material beyond the scope of the copyright law shall require the prior written consent of its respective author or creator. Downloads and copies of this site are only permitted for private, non-commercial use. Insofar as the content on this site was not created by the operator, the copyrights of third parties are respected. In particular, third-party content is identified as such. Should you nevertheless become aware of a copyright infringement, please inform us accordingly. If we become aware of any infringements, we will remove such content immediately. </p>
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
            Alexander Schönhuth
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
				Current version: v:2.2.2
			</div>
		</div>
	</div>

</template>

<script setup lang="js">
</script>

<style scoped>

.impressum, .disclaimer {
	padding: 1rem;
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

h3{
  @apply text-lg lg:text-xl font-semibold mb-2;
}

h2{
  @apply text-xl lg:text-2xl font-semibold mb-2;
}

p, strong{
  @apply text-justify leading-tight mb-2 select-none;
}

ul{
  @apply list-disc pl-8
}

li{
  @apply text-justify
}
</style>
