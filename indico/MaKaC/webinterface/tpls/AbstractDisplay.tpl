<% import MaKaC.webinterface.urlHandlers as urlHandlers %>
<% from MaKaC.paperReviewing import ConferencePaperReview as CPR %>
<% from MaKaC.review import AbstractStatusWithdrawn %>

<script type="text/javascript"
  src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
</script>
<script type="text/javascript"
  src="http://pmgaudencio.neei.uevora.pt/mathjax/mathjax-editing.js">
</script>

<script type="text/x-mathjax-config">
  MathJax.Hub.Config({"HTML-CSS": { 
    preferredFont: "TeX",
    availableFonts: ["STIX","TeX"],
    linebreaks: { automatic:true },
    EqnChunk: (MathJax.Hub.Browser.isMobile ? 10 : 50) },
    tex2jax: { inlineMath: [
        ["$", "$"],
        ["\\\\(","\\\\)"]
    ],
    displayMath: [
        ["$$","$$"],
        ["\\[", "\\]"]
    ],
    processEscapes: true,
    ignoreClass: "tex2jax_ignore|dno" },
    TeX: {  
        noUndefined: { 
            attributes: { 
                mathcolor: "red",
                mathbackground: "#FFEEEE",
                mathsize: "90%" }
            },
        Macros: {
            href: "{}"
        }
    },
    messageStyle: "none"
    });

</script>

<div id="buttonBar" class="abstractButtonBar">
    % if abstract.canModify(accessWrapper):
        % if not modifyDisabled:
            <a href="${modifyURL}" style="font-weight:bold" >${_("Edit")}</a> |
        % endif
        % if isinstance(abstract.getCurrentStatus(), AbstractStatusWithdrawn):
            <a href="${recoverURL}">${_("Recover")}</a> |
        % elif not withdrawDisabled:
            <a href="${withdrawURL}" ">${_("Withdraw")}</a> |
        % endif
    % endif
    <a href="${str(urlHandlers.UHAbstractDisplayPDF.getURL(abstract))}" target="_blank">${_("PDF")}</a>
</div>
<h1 class="abstractTitle">
    ${abstract.getTitle()}
</h1>
<div>
    <div class="abstractMainContent">
        <div class="abstractInformation">
            <div class="abstractSubmitter">
                ${_("Submitted by")} <span style="font-weight: bold">${abstract.getSubmitter().getStraightFullName()} </span>
                ${_("on")}
                <span style="font-weight: bold">${formatDate(abstract.getSubmissionDate())}</span>
                ${_("at")}
                <span style="font-weight: bold">${formatTime(abstract.getSubmissionDate())}</span>
            </div>
            <div class="abstractHeader">
                <div>
                    <span style="font-weight:bold">${_("Id")}:</span>
                    ${abstract.getId()}
                </div>
                <div>
                    <span style="font-weight: bold">${_("Last modification")}:</span>
                    ${formatDate(abstract.getModificationDate())} ${formatTime(abstract.getModificationDate())}
                </div>
                % if contribType:
                <div>
                    <span style="font-weight:bold">${_("Contribution type")}:</span>
                    ${contribType.getName()}
                </div>
                % endif
                % if False:
                <div>
                    <span style="font-weight:bold">${_("Track classification")}:</span>
                    ${",".join([t.getTitle() for t in tracks])}
                </div>
                % endif
            </div>
        </div>
        <div class="abstractDetail">
            % for f in abstract.getConference().getAbstractMgr().getAbstractFieldsMgr().getActiveFields():
                    % if abstract.getField(f.getId()):
                    <div class="abstractSection">
                        <h2 class="abstractSectionTitle">${f.getName()}</h2>
                        <div class="wmd-panel">
                            <div id="wmd-button-bar-${f.getName()}" style="display: none;"></div>
                            <textarea class="wmd-input" id="wmd-input-${f.getName()}" style="display: none;">${abstract.getField(f.getId()) | h}</textarea>
                        </div>

                        <div id="wmd-preview-${f.getName()}" class="wmd-panel wmd-preview" style="background: white"></div>
                        <div class="abstractSectionContent"></div>
                    </div>
                    % endif
            % endfor
            % if abstract.getComments():
                <div class="abstractSection">
                    <h2 class="abstractSectionTitle">${_("Comments")}</h2>
                    <div class="abstractSectionContent">${abstract.getComments()}</div>
                </div>
            % endif
        </div>
    </div>

    <div class="abstractRightPanel">

        <div class="abstractStatusSection" style="border-bottom:1px solid #eaeaea; padding-bottom:5px;">
            <h2 class="abstractSectionTitle">${_("Abstract status")}</h2>
            <div>
                <div class="abstractStatus ${statusClass}">${statusText}</div>
            </div>
        </div>
        % if abstract.getPrimaryAuthorList():
            <div class="abstractRightPanelSection">
                <h2 class="abstractSectionTitle">${_("Primary authors")}</h2>
                <ul>
                % for pa in abstract.getPrimaryAuthorList():
                    <li>${pa.getStraightFullName()}
                        (${pa.getAffiliation()})
                % endfor
                </ul>
            </div>
        % endif
        % if abstract.getCoAuthorList():
            <div class="abstractRightPanelSection">
                <h2 class="abstractSectionTitle">${_("Co-authors")}</h2>
                <ul>
                % for ca in abstract.getCoAuthorList():
                    <li>${ca.getStraightFullName()}
                        (${ca.getAffiliation()})
                % endfor
                </ul>
            </div>
        % endif
        % if abstract.getSpeakerList():
            <div class="abstractRightPanelSection">
                <h2 class="abstractSectionTitle">${_("Presenters")}</h2>
                <ul>
                % for sp in abstract.getSpeakerList():
                    <li>${sp.getStraightFullName()}
                        (${sp.getAffiliation()})
                % endfor
                </ul>
            </div>
        % endif
        % if len(attachments) != 0:
            <div class="abstractRightPanelSection">
                <h2 class="abstractSectionTitle">${_("Attached files")}</h2>
                <ul>
                    % for file in attachments:
                        <li><a href="${file['url']}">${ file["file"]["fileName"] }</a>
                    % endfor
                </ul>
            </div>
        % endif
    </div>
</div>
<script type="text/javascript">
% if statusComments:
    $(".abstractStatus").qtip({
        content: " ${statusComments}",
        position :{
            at: "bottom middle",
            my: "top middle"
        }
    });
% endif


// Pagedown editor stuff

(function () {
    % for f in abstract.getConference().getAbstractMgr().getAbstractFieldsMgr().getActiveFields():
        % if abstract.getField(f.getId()):
            var converter = Markdown.getSanitizingConverter();

            converter.hooks.chain("preBlockGamut", function (text, rbg) {
                return text.replace(/^ {0,3}""" *\n((?:.*?\n)+?) {0,3}""" *$/gm, function (whole, inner) {
                    return "<blockquote>" + rbg(inner) + "</blockquote>\n";
                });
            });

            var editor = new Markdown.Editor(converter, "-${f.getName()}");

            editor.run();
        % endif
    % endfor

})();

</script>